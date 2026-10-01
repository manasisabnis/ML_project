import streamlit as st
import subprocess
import os
import sys
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Music Generation",
    layout="centered"
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       Main background
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(109, 40, 217, 0.40),
                transparent 32%
            ),
            radial-gradient(
                circle at 95% 15%,
                rgba(37, 99, 235, 0.35),
                transparent 35%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(147, 51, 234, 0.30),
                transparent 42%
            ),
            #080d1a;

        color: #f5f7ff;
    }


    /* --------------------------------------------------------
       Page width and spacing
    -------------------------------------------------------- */

    .block-container {
        max-width: 900px;
        padding-top: 3.5rem;
        padding-bottom: 4rem;
    }


    /* --------------------------------------------------------
       Main title
    -------------------------------------------------------- */

    h1 {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -1px;
        margin-bottom: 0.5rem;
    }


    /* --------------------------------------------------------
       Section headings
    -------------------------------------------------------- */

    h2 {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 650 !important;
    }

    h3 {
        color: #ffffff !important;
        font-size: 1.55rem !important;
        font-weight: 600 !important;
    }


    /* --------------------------------------------------------
       Subtitle
    -------------------------------------------------------- */

    .subtitle {
        color: #b8c2d9;
        font-size: 1.15rem;
        line-height: 1.6;
        margin-bottom: 2.2rem;
    }


    /* --------------------------------------------------------
       Settings card
    -------------------------------------------------------- */

    .settings-card {
        background: rgba(18, 25, 46, 0.90);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 18px;
        padding: 1.8rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.30);
    }


    /* --------------------------------------------------------
       Slider labels
    -------------------------------------------------------- */

    .stSlider label {
        color: #e9edfa !important;
        font-size: 1.12rem !important;
        font-weight: 500 !important;
    }


    /* Slider text */
    .stSlider p {
        font-size: 1.05rem !important;
    }


    /* Slider numbers */
    [data-testid="stSlider"] {
        font-size: 1.05rem !important;
    }


    /* --------------------------------------------------------
       Settings summary
    -------------------------------------------------------- */

    .settings-summary {
        color: #b8c2d9;
        font-size: 1.1rem;
        margin-top: 1rem;
    }


    /* --------------------------------------------------------
       Generate button
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        min-height: 3.2rem;

        border-radius: 11px;

        border: 1px solid rgba(167, 139, 250, 0.55);

        background:
            linear-gradient(
                135deg,
                #4f46e5,
                #7c3aed
            );

        color: #ffffff;

        font-size: 1.15rem !important;
        font-weight: 600;

        box-shadow:
            0 8px 25px rgba(79, 70, 229, 0.25);

        transition: all 0.2s ease;
    }


    .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );

        border-color: #c4b5fd;

        transform: translateY(-1px);

        box-shadow:
            0 10px 30px rgba(124, 58, 237, 0.35);
    }


    /* --------------------------------------------------------
       Result card
    -------------------------------------------------------- */

    .result-card {
        background: rgba(18, 25, 46, 0.94);

        border: 1px solid rgba(129, 140, 248, 0.35);

        border-radius: 18px;

        padding: 1.8rem;

        margin-top: 1.5rem;
        margin-bottom: 1.2rem;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.30);
    }


    /* --------------------------------------------------------
       Metric cards
    -------------------------------------------------------- */

    [data-testid="stMetric"] {
        background: rgba(31, 41, 72, 0.85);

        border: 1px solid rgba(148, 163, 184, 0.18);

        border-radius: 13px;

        padding: 1.2rem;
    }


    [data-testid="stMetricLabel"] {
        color: #b8c2d9 !important;
        font-size: 1.05rem !important;
    }


    [data-testid="stMetricValue"] {
        color: #ffffff !important;

        font-size: 2.2rem !important;

        font-weight: 650 !important;
    }


    /* --------------------------------------------------------
       Download button
    -------------------------------------------------------- */

    .stDownloadButton > button {
        width: 100%;

        min-height: 3rem;

        border-radius: 11px;

        background: rgba(37, 99, 235, 0.25);

        border: 1px solid rgba(96, 165, 250, 0.50);

        color: #ffffff;

        font-size: 1.1rem !important;

        font-weight: 600;
    }


    .stDownloadButton > button:hover {
        background: rgba(37, 99, 235, 0.40);

        border-color: #60a5fa;
    }


    /* --------------------------------------------------------
       Information section
    -------------------------------------------------------- */

    .info-card {
        background: rgba(18, 25, 46, 0.82);

        border: 1px solid rgba(148, 163, 184, 0.17);

        border-radius: 18px;

        padding: 1.9rem;

        margin-top: 1rem;

        color: #dce2f0;

        font-size: 1.12rem;

        line-height: 1.9;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.20);
    }


    /* --------------------------------------------------------
       Model information expander
    -------------------------------------------------------- */

    [data-testid="stExpander"] {
        background: rgba(18, 25, 46, 0.78);

        border: 1px solid rgba(148, 163, 184, 0.18);

        border-radius: 13px;
    }


    [data-testid="stExpander"] p {
        color: #dce2f0 !important;

        font-size: 1.08rem !important;

        line-height: 1.75;
    }


    /* --------------------------------------------------------
       Divider
    -------------------------------------------------------- */

    hr {
        border-color: rgba(148, 163, 184, 0.16);

        margin-top: 2.8rem;
        margin-bottom: 2.8rem;
    }


    /* --------------------------------------------------------
       Caption
    -------------------------------------------------------- */

    .stCaption {
        color: #aeb8ce !important;

        font-size: 1.05rem !important;
    }


    /* --------------------------------------------------------
       Success / error messages
    -------------------------------------------------------- */

    [data-testid="stAlert"] {
        border-radius: 11px;

        font-size: 1.05rem;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<h1>Music Generation</h1>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Generate new musical sequences using an LSTM trained on MIDI data.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GENERATION SETTINGS
# ============================================================

st.markdown(
    '<div class="settings-card">',
    unsafe_allow_html=True
)

st.subheader("Generation settings")

col1, col2 = st.columns(2)

with col1:

    temperature = st.slider(
        "Temperature",
        min_value=0.5,
        max_value=1.3,
        value=0.8,
        step=0.1,
        format="%.1f",
        help=(
            "Higher temperatures allow more variation "
            "in the generated music."
        )
    )


with col2:

    generate_length = st.slider(
        "Number of musical events",
        min_value=50,
        max_value=500,
        value=200,
        step=50
    )


st.markdown(
    f"""
    <div class="settings-summary">
        Temperature: <strong>{temperature:.1f}</strong>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        Events: <strong>{generate_length}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    "Generate music",
    type="primary"
):

    with st.spinner("Generating music..."):

        generate_file = "src/generate.py"

        # Read generate.py
        with open(
            generate_file,
            "r"
        ) as f:

            code = f.read()


        # Replace temperature
        code = re.sub(
            r"TEMPERATURE\s*=\s*[0-9.]+",
            f"TEMPERATURE = {temperature}",
            code
        )


        # Replace generation length
        code = re.sub(
            r"GENERATE_LENGTH\s*=\s*[0-9]+",
            f"GENERATE_LENGTH = {generate_length}",
            code
        )


        # Save updated settings
        with open(
            generate_file,
            "w"
        ) as f:

            f.write(code)


        # Run generation
        result = subprocess.run(
            [
                sys.executable,
                generate_file
            ],
            capture_output=True,
            text=True
        )


    # ========================================================
    # SUCCESS
    # ========================================================

    if result.returncode == 0:

        output_file = (
            f"output/"
            f"generated_temperature_{temperature}.mid"
        )

        if os.path.exists(output_file):

            st.success(
                "Music generated successfully."
            )


            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.subheader("Generated music")

            metric_col1, metric_col2 = st.columns(2)

            with metric_col1:

                st.metric(
                    "Temperature",
                    f"{temperature:.1f}"
                )

            with metric_col2:

                st.metric(
                    "Musical events",
                    generate_length
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # Download
            # ------------------------------------------------

            with open(
                output_file,
                "rb"
            ) as f:

                st.download_button(
                    label="Download MIDI",
                    data=f,
                    file_name=(
                        f"generated_music_"
                        f"temperature_{temperature}.mid"
                    ),
                    mime="audio/midi"
                )


        else:

            st.error(
                "Generation completed, but the MIDI file "
                "could not be found."
            )


    # ========================================================
    # ERROR
    # ========================================================

    else:

        st.error(
            "An error occurred during music generation."
        )

        with st.expander("View error details"):

            st.code(
                result.stderr
            )


# ============================================================
# HOW IT WORKS
# ============================================================

st.divider()

st.subheader("How it works")

st.markdown(
    """
    <div class="info-card">

    The model is trained on MIDI files from the MAESTRO dataset.
    Notes and chords are extracted and arranged into sequences
    of 40 musical events.

    <br>

    The LSTM learns patterns in these sequences and predicts
    the next musical event. This process is repeated to create
    a new sequence, which is then converted into a MIDI file.

    <br>

    The temperature setting controls how much variation is
    allowed when choosing the next musical event.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MODEL INFORMATION
# ============================================================

st.divider()

with st.expander("Model information"):

    st.write(
        "The project uses a Long Short-Term Memory (LSTM) "
        "neural network for sequence prediction."
    )

    st.write(
        "The model uses 128 LSTM units, a dropout rate of 0.3, "
        "the Adam optimizer and sparse categorical crossentropy."
    )

    st.write(
        "The model was trained for 10 epochs using a sequence "
        "length of 40 musical events."
    )