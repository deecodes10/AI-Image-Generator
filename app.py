import streamlit as st
import os
import io
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS — PASTEL UI
# --------------------------------------------------

st.markdown("""
<style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background: linear-gradient(
            135deg,
            #fff4f8 0%,
            #f7f0ff 50%,
            #eef7ff 100%
        );
    }


    /* ---------- MAIN CONTENT WIDTH ---------- */

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }


    /* ---------- TITLE ---------- */

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 800;
        color: #6d5a8d;
        margin-bottom: 8px;
    }


    /* ---------- SUBTITLE ---------- */

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #8b7c9f;
        margin-bottom: 45px;
    }


    /* ---------- SECTION TITLES ---------- */

    .section-title {
        font-size: 27px;
        font-weight: 700;
        color: #765b91;
        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* ---------- INPUT LABELS ---------- */

    label {
        color: #705b83 !important;
        font-weight: 600 !important;
    }


    /* ---------- TEXT AREA ---------- */

    textarea {
        background-color: #fffafd !important;
        border: 2px solid #eadcf4 !important;
        border-radius: 16px !important;
        color: #554661 !important;
    }

    textarea:focus {
        border-color: #c9a7e8 !important;
        box-shadow: 0 0 0 2px #eadcf4 !important;
    }


    /* ---------- SELECT BOX ---------- */

    div[data-baseweb="select"] > div {
        background-color: #fffafd !important;
        border: 2px solid #eadcf4 !important;
        border-radius: 14px !important;
    }


    /* ---------- GENERATE BUTTON ---------- */

    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 16px;
        border: none;
        background: linear-gradient(
            90deg,
            #d9a7e8,
            #f3a9c8
        );
        color: white;
        font-size: 17px;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(180, 130, 190, 0.25);
        transition: 0.2s;
    }


    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(180, 130, 190, 0.35);
    }


    /* ---------- DOWNLOAD BUTTON ---------- */

    .stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        border: 2px solid #e4cfee;
        background: #fffafd;
        color: #765b91;
        font-weight: 600;
    }


    .stDownloadButton > button:hover {
        background: #f8efff;
        border-color: #c9a7e8;
    }


    /* ---------- SUCCESS MESSAGE ---------- */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ---------- IMAGE ROUNDED CORNERS ---------- */

    img {
        border-radius: 18px;
    }


    /* ---------- DIVIDER ---------- */

    hr {
        border: none;
        height: 2px;
        background: #eadcf4;
        margin-top: 35px;
        margin-bottom: 35px;
    }


    /* ---------- HISTORY INFO ---------- */

    .history-info {
        background: rgba(255, 250, 253, 0.85);
        border: 2px solid #eadcf4;
        border-radius: 16px;
        padding: 15px 20px;
        margin-bottom: 15px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #9b8baa;
        font-size: 14px;
        margin-top: 50px;
        padding-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

load_dotenv()

token = os.getenv("HF_TOKEN")

if not token:
    st.error("HF_TOKEN not found. Please check your .env file.")
    st.stop()


# --------------------------------------------------
# HUGGING FACE CLIENT
# --------------------------------------------------

client = InferenceClient(
    provider="nscale",
    api_key=token
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "history" not in st.session_state:
    st.session_state.history = []


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎨 AI Image Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '✨ Turn your imagination into beautiful AI-generated images ✨'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# CREATE IMAGE
# --------------------------------------------------

st.markdown(
    '<div class="section-title">✨ Create Your Image</div>',
    unsafe_allow_html=True
)


# Prompt
prompt = st.text_area(
    "Describe your image",
    placeholder=(
        "Example: A cute little café in Paris at sunset, "
        "flowers around the windows, dreamy atmosphere..."
    ),
    height=120
)


# Controls
col1, col2 = st.columns(2)

with col1:

    style = st.selectbox(
        "🎨 Image Style",
        [
            "Realistic",
            "Anime",
            "Cartoon",
            "Digital Art",
            "Oil Painting",
            "Cinematic",
            "3D Render"
        ]
    )


with col2:

    num_images = st.selectbox(
        "🖼️ Number of Images",
        [1, 2, 3, 4]
    )


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

st.write("")

if st.button("✨ Generate Images"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt first.")

    else:

        final_prompt = f"{prompt}, {style} style"

        with st.spinner(
            f"Creating {num_images} beautiful image(s)..."
        ):

            try:

                generated_images = []

                for i in range(num_images):

                    image = client.text_to_image(
                        prompt=final_prompt,
                        model="black-forest-labs/FLUX.1-schnell"
                    )

                    generated_images.append(image)

                    # Save to history
                    st.session_state.history.append({
                        "prompt": prompt,
                        "style": style,
                        "image": image
                    })


                st.success(
                    f"✨ {num_images} image(s) generated successfully!"
                )


                # --------------------------------------------------
                # GENERATED IMAGES
                # --------------------------------------------------

                st.markdown(
                    '<div class="section-title">'
                    '🖼️ Your Creations'
                    '</div>',
                    unsafe_allow_html=True
                )


                if num_images == 1:

                    columns = st.columns(1)

                else:

                    columns = st.columns(2)


                for i, image in enumerate(generated_images):

                    with columns[i % len(columns)]:

                        st.image(
                            image,
                            caption=f"✨ Generated Image {i + 1}",
                            use_container_width=True
                        )


                        img_bytes = io.BytesIO()

                        image.save(
                            img_bytes,
                            format="PNG"
                        )


                        st.download_button(
                            label=f"⬇️ Download Image {i + 1}",
                            data=img_bytes.getvalue(),
                            file_name=f"generated_image_{i + 1}.png",
                            mime="image/png",
                            key=f"download_current_{i}"
                        )


            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# --------------------------------------------------
# GENERATION HISTORY
# --------------------------------------------------

if st.session_state.history:

    st.markdown(
        '<div class="section-title">'
        '📜 Your Generation History'
        '</div>',
        unsafe_allow_html=True
    )


    for index, item in enumerate(
        reversed(st.session_state.history)
    ):

        st.markdown(
            '<div class="history-info">',
            unsafe_allow_html=True
        )

        st.write(
            f"**💭 Prompt:** {item['prompt']}"
        )

        st.write(
            f"**🎨 Style:** {item['style']}"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        st.image(
            item["image"],
            caption="Previous Generation",
            use_container_width=True
        )


        history_bytes = io.BytesIO()

        item["image"].save(
            history_bytes,
            format="PNG"
        )


        st.download_button(
            label="⬇️ Download",
            data=history_bytes.getvalue(),
            file_name=f"history_image_{index + 1}.png",
            mime="image/png",
            key=f"history_download_{index}"
        )


        st.divider()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    '<div class="footer">'
    '🌸 AI Image Studio • Powered by Hugging Face FLUX 🌸'
    '</div>',
    unsafe_allow_html=True
)