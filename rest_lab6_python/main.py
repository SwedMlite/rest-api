import os

import uvicorn


def main():
    port = int(os.getenv("APP_PORT", os.getenv("PORT", "8080")))
    reload = os.getenv("UVICORN_RELOAD", "false").lower() == "true"
    target_app = os.getenv("UVICORN_APP", "rest_lab6_python.app.main:app")
    uvicorn.run(target_app, host="0.0.0.0", port=port, reload=reload)


if __name__ == "__main__":
    main()
