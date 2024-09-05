import os

from flask import Flask, render_template, url_for

from bot.config import PORT, UPLOAD_FOLDER

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/view_photos/<int:user_id>", methods=["GET"])
def view_photos(user_id):
    """Отображение фотографий пользователя."""
    try:
        all_photos = os.listdir(UPLOAD_FOLDER)

        user_photos = [
            photo for photo in all_photos if photo.startswith(f"{user_id}_")
        ]

        photos = [
            url_for("static", filename=f"uploads/{photo}")
            for photo in user_photos
        ]

        return render_template("view_photos.html", photos=photos)
    except Exception as e:
        return f"Произошла ошибка при получении фотографий: {e}"


@app.route("/photos")
def show_photos():
    """Отображение всех фотографий для админа."""
    photos_by_user = {}

    all_photos = os.listdir(UPLOAD_FOLDER)
    for photo in all_photos:
        user_id = photo.split("_")[0]
        if user_id not in photos_by_user:
            photos_by_user[user_id] = []
        photos_by_user[user_id].append(photo)

    return render_template("photos.html", photos_by_user=photos_by_user)


def run_flask():
    app.run(debug=True, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run_flask()
