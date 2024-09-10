from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]  # Change to your specific allowed origins


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
