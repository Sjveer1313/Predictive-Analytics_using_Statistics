import streamlit as st
import os
import yt_dlp
from pydub import AudioSegment
import zipfile
import re
import smtplib
from email.message import EmailMessage


def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def download_videos(singer, count):
    search_query = f"ytsearch{count}:{singer}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

def create_mashup(duration, output_file):
    combined = AudioSegment.empty()

    for file in os.listdir("downloads"):
        path = os.path.join("downloads", file)

        try:
            audio = AudioSegment.from_file(path)
            clip = audio[:duration * 1000]
            combined += clip
        except:
            pass

    combined.export(output_file, format="mp3")

def send_email(receiver, zip_file):

    sender = "ssingh33_be23@thapar.edu"
    password = "tmer ryom wanw hhko"

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender
    msg["To"] = receiver

    with open(zip_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="zip",
            filename=zip_file
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# Streamlit UI

st.title("🎵 YouTube Mashup Generator")

singer = st.text_input("Enter Singer Name : ")
num_videos = st.number_input("Number of Videos ( >10 ) : ", min_value=11)
duration = st.number_input("Duration of each video in seconds ( >20 ) : ", min_value=21)
email = st.text_input("Enter Email ID : ")

if st.button("Create Mashup"):

    if not singer:
        st.error("Please enter singer name.")
    elif not valid_email(email):
        st.error("Invalid email address.")
    else:
        try:
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            st.info("Downloading videos...")
            download_videos(singer, num_videos)

            output_file = "mashup.mp3"

            st.info("Creating mashup...")
            create_mashup(duration, output_file)

            zip_name = "result.zip"
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                zipf.write(output_file)

            st.info("Sending email...")
            send_email(email, zip_name)

            st.success("Mashup created and sent successfully!")

        except Exception as e:
            st.error(f"Error: {e}")
