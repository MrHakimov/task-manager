from common import get_app

__all__ = [
    'app',
]

app = get_app()

if __name__ == '__main__':
    app.run()
