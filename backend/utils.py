def analysis(video) -> tuple:
    """Function to perform analysis."""
    if video.lang:
        # generate word cloud
        comment_text = " ".join(video.__dict__.get("comments"))

        filename = generate_word_cloud(
            video.id_.get_id(), extract_all_descriptive_words(comment_text), video.lang)
    else:
        filename = ""

    # sentiment analysis
    return sentiment_analysis(comment_text), filename


if __name__ == "__main__":
    pass