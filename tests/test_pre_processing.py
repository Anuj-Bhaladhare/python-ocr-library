"""
Professional OCR Pre-processing Pipeline
Author: OCR Engine
Date: 2024
Description: Complete pre-processing pipeline for OCR with image enhancement capabilities
"""

import os
import sys
import logging
import numpy as np
import cv2
from typing import Optional, Tuple, Dict, Any, Union
from dataclasses import dataclass
from pathlib import Path
import matplotlib.pyplot as plt
from skimage import io, transform, exposure, filters, restoration
from skimage.util import img_as_ubyte, img_as_float
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingConfig:
    """Configuration for image processing parameters"""
    # Image enhancement
    gamma: float = 1.2
    contrast: float = 1.5
    sharpen: bool = True
    
    # Binarization
    threshold_method: str = 'adaptive'  # 'adaptive', 'otsu', 'sauvola'
    block_size: int = 11
    C: int = 2
    
    # Noise reduction
    denoise_strength: float = 10.0
    bilateral_filter: bool = True
    bilateral_d: int = 9
    bilateral_sigma_color: float = 75
    bilateral_sigma_space: float = 75
    
    # Deskewing
    min_angle: float = -45.0
    max_angle: float = 45.0
    angle_step: float = 0.5
    
    # Layout analysis
    min_text_size: int = 10
    max_text_size: int = 100
    text_margin: int = 5
    
    # Output
    show_steps: bool = False
    save_intermediate: bool = False
    output_dir: str = "processed_output"


class ImagePreprocessor:
    """Professional-grade image preprocessor for OCR pipeline"""
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Initialize the preprocessor with configuration.
        
        Args:
            config: ProcessingConfig object with processing parameters
        """
        self.config = config or ProcessingConfig()
        self.original_image: Optional[np.ndarray] = None
        self.processed_image: Optional[np.ndarray] = None
        self.metadata: Dict[str, Any] = {}
        
        # Create output directory if needed
        if self.config.save_intermediate:
            os.makedirs(self.config.output_dir, exist_ok=True)
    
    def _save_intermediate(self, image: np.ndarray, step_name: str) -> None:
        """Save intermediate processing step if configured"""
        if self.config.save_intermediate:
            output_path = os.path.join(self.config.output_dir, f"{step_name}.png")
            cv2.imwrite(output_path, image)
            logger.debug(f"Saved intermediate image: {output_path}")
    
    def _visualize_step(self, image: np.ndarray, title: str, cmap: str = 'gray') -> None:
        """Visualize processing step if configured"""
        if self.config.show_steps:
            plt.figure(figsize=(10, 6))
            plt.imshow(image, cmap=cmap)
            plt.title(title)
            plt.axis('off')
            plt.tight_layout()
            plt.show()
    
    # STEP-1: Image Acquisition
    def acquire_image(self, 
                     source: Union[str, np.ndarray, Image.Image], 
                     source_type: str = 'file') -> np.ndarray:
        """
        Acquire image from various sources.
        
        Args:
            source: Image source (file path, numpy array, or PIL Image)
            source_type: Type of source ('file', 'array', 'pil')
            
        Returns:
            numpy.ndarray: Loaded image in BGR format
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If source type is invalid or image cannot be loaded
        """
        logger.info("STEP-1: Image Acquisition")
        
        try:
            if source_type == 'file':
                if not os.path.exists(source):
                    raise FileNotFoundError(f"Image file not found: {source}")
                
                # Load image using OpenCV (preserves color channels)
                self.original_image = cv2.imread(source)
                if self.original_image is None:
                    # Try alternative loading method
                    self.original_image = io.imread(source)
                    if len(self.original_image.shape) == 3 and self.original_image.shape[2] == 4:
                        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGBA2BGR)
                    elif len(self.original_image.shape) == 3:
                        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2BGR)
                
            elif source_type == 'array':
                self.original_image = source.copy()
                if len(self.original_image.shape) == 3 and self.original_image.shape[2] == 3:
                    # Assume RGB, convert to BGR for OpenCV
                    self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2BGR)
            
            elif source_type == 'pil':
                self.original_image = cv2.cvtColor(np.array(source), cv2.COLOR_RGB2BGR)
            
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            if self.original_image is None:
                raise ValueError("Failed to load image from source")
            
            # Store metadata
            self.metadata['original_shape'] = self.original_image.shape
            self.metadata['original_dtype'] = self.original_image.dtype
            self.metadata['channels'] = self.original_image.shape[2] if len(self.original_image.shape) == 3 else 1
            
            logger.info(f"Image acquired: {self.original_image.shape}, dtype: {self.original_image.dtype}")
            self._visualize_step(cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB), 
                               "Original Image", cmap=None)
            self._save_intermediate(self.original_image, "01_original")
            
            return self.original_image
            
        except Exception as e:
            logger.error(f"Image acquisition failed: {str(e)}")
            raise
    
    # STEP-2: Image Loading and Validation
    def load_and_validate(self, image: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Load and validate image for processing.
        
        Args:
            image: Optional image array, uses original if None
            
        Returns:
            numpy.ndarray: Validated image
        """
        logger.info("STEP-2: Image Loading and Validation")
        
        if image is None:
            if self.original_image is None:
                raise ValueError("No image loaded. Call acquire_image() first.")
            image = self.original_image
        
        # Validate image properties
        if len(image.shape) not in [2, 3]:
            raise ValueError(f"Invalid image shape: {image.shape}")
        
        if image.dtype not in [np.uint8, np.float32, np.float64]:
            logger.warning(f"Converting image from {image.dtype} to uint8")
            if image.dtype == np.float32 or image.dtype == np.float64:
                image = img_as_ubyte(image)
            else:
                image = image.astype(np.uint8)
        
        # Check for empty image
        if image.size == 0:
            raise ValueError("Image is empty")
        
        # Check for all black or all white images
        if len(image.shape) == 2:
            unique_vals = np.unique(image)
            if len(unique_vals) == 1:
                logger.warning("Image appears to be uniform (all same pixel value)")
        
        self.metadata['validated_shape'] = image.shape
        logger.info(f"Image validated successfully: {image.shape}")
        
        return image
    
    # STEP-3: Grayscale Conversion
    def convert_to_grayscale(self, image: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Convert image to grayscale if it's a color image.
        
        Args:
            image: Input image, uses processed image if None
            
        Returns:
            numpy.ndarray: Grayscale image
        """
        logger.info("STEP-3: Grayscale Conversion")
        
        if image is None:
            image = self.load_and_validate()
        
        if len(image.shape) == 3:
            # Convert BGR to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image.copy()
        
        self._visualize_step(gray_image, "Grayscale Image")
        self._save_intermediate(gray_image, "03_grayscale")
        logger.info(f"Grayscale conversion complete: {gray_image.shape}")
        
        return gray_image
    
    # STEP-4: Noise Reduction
    def reduce_noise(self, image: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Apply noise reduction techniques.
        
        Args:
            image: Input grayscale image
            
        Returns:
            numpy.ndarray: Denoised image
        """
        logger.info("STEP-4: Noise Reduction")
        
        if image is None:
            image = self.convert_to_grayscale()
        
        # Convert to float for processing
        image_float = img_as_float(image)
        
        # Apply Non-local Means Denoising
        denoised = restoration.denoise_nl_means(
            image_float,
            h=self.config.denoise_strength * 0.1,
            fast_mode=True,
            patch_size=5,
            patch_distance=6
        )
        
        # Convert back to uint8
        denoised = img_as_ubyte(np.clip(denoised, 0, 1))
        
        # Optional bilateral filtering for edge preservation
        if self.config.bilateral_filter:
            denoised = cv2.bilateralFilter(
                denoised,
                d=self.config.bilateral_d,
                sigmaColor=self.config.bilateral_sigma_color,
                sigmaSpace=self.config.bilateral_sigma_space
            )
        
        self._visualize_step(denoised, "Noise Reduced Image")
        self._save_intermediate(denoised, "04_noise_reduced")
        logger.info("Noise reduction complete")
        
        return denoised
    
    # STEP-5: Binarization (Thresholding)
    def binarize_image(self, image: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Convert image to binary (black and white).
        
        Args:
            image: Input grayscale image
            
        Returns:
            numpy.ndarray: Binary image
        """
        logger.info("STEP-5: Binarization")
        
        if image is None:
            image = self.reduce_noise()
        
        if self.config.threshold_method == 'adaptive':
            # Adaptive Gaussian thresholding
            binary = cv2.adaptiveThreshold(
                image,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                self.config.block_size,
                self.config.C
            )
            
        elif self.config.threshold_method == 'otsu':
            # Otsu's thresholding
            _, binary = cv2.threshold(
                image, 0, 255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            
        elif self.config.threshold_method == 'sauvola':
            # Sauvola's local thresholding
            from skimage.filters import threshold_sauvola
            thresh_sauvola = threshold_sauvola(image, window_size=25)
            binary = (image > thresh_sauvola).astype(np.uint8) * 255
            
        else:
            raise ValueError(f"Unknown threshold method: {self.config.threshold_method}")
        
        # Invert if needed (white text on black background)
        if np.mean(binary) > 127:
            binary = cv2.bitwise_not(binary)
        
        # Apply morphological operations to clean up
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        self._visualize_step(binary, "Binarized Image")
        self._save_intermediate(binary, "05_binarized")
        logger.info(f"Binarization complete using {self.config.threshold_method} method")
        
        return binary
    
    # STEP-6: Deskewing (Rotation Correction)
    def deskew_image(self, image: Optional[np.ndarray] = None) -> Tuple[np.ndarray, float]:
        """
        Correct image skew/rotation.
        
        Args:
            image: Input binary image
            
        Returns:
            Tuple[numpy.ndarray, float]: Deskewed image and rotation angle
        """
        logger.info("STEP-6: Deskewing")
        
        if image is None:
            image = self.binarize_image()
        
        # Make a copy for processing
        binary = image.copy()
        
        # Invert if needed for Hough transform
        if np.mean(binary) < 127:
            binary = cv2.bitwise_not(binary)
        
        # Detect edges
        edges = cv2.Canny(binary, 50, 150, apertureSize=3)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        angles = []
        if lines is not None:
            for rho, theta in lines[:, 0]:
                angle = theta * 180 / np.pi - 90
                if self.config.min_angle <= angle <= self.config.max_angle:
                    angles.append(angle)
        
        if angles:
            # Calculate median angle (more robust than mean)
            median_angle = np.median(angles)
            
            # Only rotate if angle is significant
            if abs(median_angle) > 0.5:
                # Get image center
                (h, w) = image.shape[:2]
                center = (w // 2, h // 2)
                
                # Rotation matrix
                M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
                
                # Calculate new bounding dimensions
                cos = np.abs(M[0, 0])
                sin = np.abs(M[0, 1])
                new_w = int((h * sin) + (w * cos))
                new_h = int((h * cos) + (w * sin))
                
                # Adjust rotation matrix
                M[0, 2] += (new_w / 2) - center[0]
                M[1, 2] += (new_h / 2) - center[1]
                
                # Apply rotation
                deskewed = cv2.warpAffine(image, M, (new_w, new_h),
                                         flags=cv2.INTER_CUBIC,
                                         borderMode=cv2.BORDER_REPLICATE)
                
                logger.info(f"Image deskewed by {median_angle:.2f} degrees")
                self.metadata['deskew_angle'] = median_angle
                
                self._visualize_step(deskewed, f"Deskewed Image (angle: {median_angle:.2f}°)")
                self._save_intermediate(deskewed, "06_deskewed")
                
                return deskewed, median_angle
        
        logger.info("No significant skew detected")
        self.metadata['deskew_angle'] = 0.0
        
        return image, 0.0
    
    # STEP-7: Layout Analysis and Text Region Detection
    def analyze_layout(self, image: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Analyze document layout and detect text regions.
        
        Args:
            image: Input binary image
            
        Returns:
            Dict containing layout information and region bounding boxes
        """
        logger.info("STEP-7: Layout Analysis")
        
        if image is None:
            image, _ = self.deskew_image()
        
        # Make a copy for visualization
        layout_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) if len(image.shape) == 2 else image.copy()
        
        # Find contours (potential text regions)
        contours, hierarchy = cv2.findContours(
            image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        text_regions = []
        non_text_regions = []
        
        for contour in contours:
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter by size
            if (self.config.min_text_size < w < self.config.max_text_size and
                self.config.min_text_size < h < self.config.max_text_size):
                
                # Calculate aspect ratio
                aspect_ratio = w / h if h > 0 else 0
                
                # Calculate area and solidity
                area = cv2.contourArea(contour)
                hull_area = cv2.contourArea(cv2.convexHull(contour))
                solidity = area / hull_area if hull_area > 0 else 0
                
                # Heuristic to identify text regions
                is_text = (
                    0.1 < aspect_ratio < 10 and  # Reasonable aspect ratio
                    solidity > 0.3 and           # Fairly solid
                    area > 20                    # Not too small
                )
                
                region_info = {
                    'bbox': (x, y, w, h),
                    'area': area,
                    'aspect_ratio': aspect_ratio,
                    'solidity': solidity,
                    'is_text': is_text
                }
                
                if is_text:
                    text_regions.append(region_info)
                    # Draw green rectangle for text regions
                    cv2.rectangle(layout_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    non_text_regions.append(region_info)
                    # Draw red rectangle for non-text regions
                    cv2.rectangle(layout_image, (x, y), (x + w, y + h), (0, 0, 255), 1)
        
        # Sort text regions by y-coordinate (top to bottom)
        text_regions.sort(key=lambda r: r['bbox'][1])
        
        # Group into lines and paragraphs
        lines = []
        current_line = []
        line_height_threshold = self.config.min_text_size * 2
        
        for region in text_regions:
            x, y, w, h = region['bbox']
            region_center_y = y + h / 2
            
            if not current_line:
                current_line.append(region)
            else:
                # Check if region is on the same line
                last_region = current_line[-1]
                last_x, last_y, last_w, last_h = last_region['bbox']
                last_center_y = last_y + last_h / 2
                
                if abs(region_center_y - last_center_y) < line_height_threshold:
                    current_line.append(region)
                else:
                    # Sort regions in line by x-coordinate
                    current_line.sort(key=lambda r: r['bbox'][0])
                    lines.append(current_line.copy())
                    current_line = [region]
        
        if current_line:
            current_line.sort(key=lambda r: r['bbox'][0])
            lines.append(current_line)
        
        # Create layout analysis result
        layout_result = {
            'text_regions': text_regions,
            'non_text_regions': non_text_regions,
            'lines': lines,
            'total_text_regions': len(text_regions),
            'total_lines': len(lines),
            'image_shape': image.shape
        }
        
        # Visualize layout
        self._visualize_step(layout_image, "Layout Analysis (Green=Text, Red=Non-text)", cmap=None)
        self._save_intermediate(layout_image, "07_layout_analysis")
        
        logger.info(f"Layout analysis complete: {len(text_regions)} text regions, {len(lines)} lines")
        
        return layout_result
    
    # Complete Preprocessing Pipeline
    def run_full_pipeline(self, image_source: Union[str, np.ndarray], 
                         source_type: str = 'file') -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Run the complete preprocessing pipeline.
        
        Args:
            image_source: Source of the image
            source_type: Type of source ('file', 'array', 'pil')
            
        Returns:
            Tuple of processed image and processing metadata
        """
        logger.info("Starting complete OCR preprocessing pipeline")
        
        try:
            # Step 1: Acquire image
            self.acquire_image(image_source, source_type)
            
            # Step 2-6: Process image
            validated = self.load_and_validate()
            grayscale = self.convert_to_grayscale(validated)
            denoised = self.reduce_noise(grayscale)
            binarized = self.binarize_image(denoised)
            deskewed, angle = self.deskew_image(binarized)
            
            # Step 7: Analyze layout
            layout_info = self.analyze_layout(deskewed)
            
            # Store final processed image
            self.processed_image = deskewed
            
            # Compile metadata
            self.metadata.update({
                'pipeline_completed': True,
                'processing_steps': [
                    'image_acquisition',
                    'validation',
                    'grayscale_conversion',
                    'noise_reduction',
                    'binarization',
                    'deskewing',
                    'layout_analysis'
                ],
                'layout_info': layout_info
            })
            
            logger.info("OCR preprocessing pipeline completed successfully")
            
            return self.processed_image, self.metadata
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def enhance_for_ocr(self, image: np.ndarray) -> np.ndarray:
        """
        Additional enhancement specifically for OCR improvement.
        
        Args:
            image: Input binary image
            
        Returns:
            numpy.ndarray: Enhanced image
        """
        logger.info("Applying OCR-specific enhancements")
        
        # Convert to PIL for enhancement
        pil_image = Image.fromarray(image)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        enhanced = enhancer.enhance(self.config.contrast)
        
        # Sharpen if configured
        if self.config.sharpen:
            enhanced = enhanced.filter(ImageFilter.SHARPEN)
        
        # Convert back to numpy
        enhanced_np = np.array(enhanced)
        
        # Apply gamma correction
        if self.config.gamma != 1.0:
            enhanced_np = exposure.adjust_gamma(enhanced_np, self.config.gamma)
        
        self._visualize_step(enhanced_np, "OCR Enhanced Image")
        self._save_intermediate(enhanced_np, "08_enhanced_for_ocr")
        
        return enhanced_np
    
    def extract_text_regions(self, image: np.ndarray, layout_info: Dict[str, Any]) -> Dict[int, np.ndarray]:
        """
        Extract individual text regions from processed image.
        
        Args:
            image: Processed binary image
            layout_info: Layout analysis results
            
        Returns:
            Dict mapping region ID to extracted region image
        """
        extracted_regions = {}
        
        for i, region in enumerate(layout_info['text_regions']):
            x, y, w, h = region['bbox']
            
            # Add margin
            x1 = max(0, x - self.config.text_margin)
            y1 = max(0, y - self.config.text_margin)
            x2 = min(image.shape[1], x + w + self.config.text_margin)
            y2 = min(image.shape[0], y + h + self.config.text_margin)
            
            # Extract region
            region_image = image[y1:y2, x1:x2]
            
            if region_image.size > 0:
                extracted_regions[i] = region_image
        
        logger.info(f"Extracted {len(extracted_regions)} text regions")
        return extracted_regions


# Example usage and test function
def main():
    """Example usage of the OCR Preprocessor"""
    
    # Create configuration
    config = ProcessingConfig(
        threshold_method='adaptive',
        block_size=15,
        C=5,
        denoise_strength=15.0,
        bilateral_filter=True,
        show_steps=True,
        save_intermediate=True
    )
    
    # Initialize preprocessor
    preprocessor = ImagePreprocessor(config)
    
    try:
        # Example 1: Process from file
        if len(sys.argv) > 1:
            image_path = sys.argv[1]
        else:
            # Use a sample image or create a test pattern
            image_path = "sample_document.jpg"
            
            # Create a test image if sample doesn't exist
            if not os.path.exists(image_path):
                logger.warning(f"Sample image not found: {image_path}")
                logger.info("Creating test pattern for demonstration...")
                
                # Create a simple test pattern
                test_image = np.ones((400, 600), dtype=np.uint8) * 255
                cv2.putText(test_image, "OCR Test Document", (50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
                cv2.putText(test_image, "Line 1: Hello World", (50, 200), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                cv2.putText(test_image, "Line 2: OCR Processing", (50, 300), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
                
                # Add some noise
                noise = np.random.normal(0, 25, test_image.shape).astype(np.uint8)
                test_image = cv2.add(test_image, noise)
                
                cv2.imwrite(image_path, test_image)
        
        # Run full pipeline
        processed_image, metadata = preprocessor.run_full_pipeline(
            image_path, 
            source_type='file'
        )
        
        # Apply OCR-specific enhancements
        enhanced_image = preprocessor.enhance_for_ocr(processed_image)
        
        # Extract text regions
        extracted_regions = preprocessor.extract_text_regions(
            enhanced_image, 
            metadata['layout_info']
        )
        
        # Print summary
        print("\n" + "="*60)
        print("OCR PREPROCESSING PIPELINE SUMMARY")
        print("="*60)
        print(f"Original Image: {metadata['original_shape']}")
        print(f"Processed Image: {processed_image.shape}")
        print(f"Text Regions Found: {metadata['layout_info']['total_text_regions']}")
        print(f"Lines Detected: {metadata['layout_info']['total_lines']}")
        print(f"Deskew Angle: {metadata.get('deskew_angle', 0):.2f}°")
        
        # Optional: Perform OCR on processed image
        try:
            # Use pytesseract for OCR (if installed)
            text = pytesseract.image_to_string(enhanced_image, config='--psm 3')
            print("\nExtracted Text Preview:")
            print("-"*40)
            print(text[:500] + "..." if len(text) > 500 else text)
        except Exception as e:
            logger.warning(f"OCR text extraction not available: {e}")
            print("\nNote: Install pytesseract for text extraction")
        
        print("\nProcessing completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Check for required dependencies
    required_packages = ['numpy', 'opencv-python', 'scikit-image', 'matplotlib', 'Pillow']
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        sys.exit(1)
    
    # Run main function
    sys.exit(main())

    