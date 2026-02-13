from pre_processing import PreProcessingPhase


def main():
    # Create object of PreProcessingPhase
    pre_process = PreProcessingPhase(data = None)


    # ----------------------------------------------------------
    # ----------------- Call All Function Here -----------------
    # ----------------------------------------------------------

    pre_process.Convert_To_Grayscale()

    pre_process.Deskewing()

    pre_process.call_remove_border()

    # pre_process.Noise_Removal()

    # pre_process.Thresholding_binarization()

    # pre_process.Erosion_Dilation()


if __name__ == "__main__":
    main()
