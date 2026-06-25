# Mini Music

Mini Music is a fast, beautiful and good, self-hosted music streaming server. Like [Swing Music](https://swingmx.com) or [Spotify](https://spotify.com/), but bring your own music in your machine.

> [!IMPORTANT]
> Mini Music is in development. The first version(0.0.1 or 0.0.2) can have some bugs, to help us, open a issue or make a Pull Request(PR).

## Features

- **Cross-Plataform(Linux, Windows, Mac, Android and iPhone)**
- **Beautiful UI using HTML and CSS**
- **Multi-user support**
- **Local Server using FastAPI**

And **More!**

## Installation

To run Mini Music on Windows, you need the Mini Music Binary.

The App should start at [http://localhost:8000](http://localhost:8000) by default. Open the URL in your browser, create or sign in with you Mini Music Account.

### Using Docker Compose

```yml
services:
  minimusic:
    image: ghcr.io/minimusic-app/minimusic:latest
    container_name: minimusic
    ports:
      - "8000:8000"
    volumes:
      - ./musics:/music
      - ./config:/config
    environment:
      - SERVER_PORT=8000
    restart: unless-stopped
```

You can set a new port for the local server. Just change the ports in the docker-compose.yml, set `SERVER_PORT` to your desired port(ex: `1970:1970` with `SERVER_PORT=1970`).

### Using Docker CLI

```bash
docker pull ghcr.io/minimusic-app/minimusic:latest
```

Then Run:

```bash
docker run --name minimusic -p 8000:8000 -e SERVER_PORT=8000 -v .musics:/music  ./config:/config --restart unless-stopped ghcr.io/minimusic-app/minimusic:latest
```

Replace the following with appropriate values:

- `./musics:/music` - Your Music Directory
- `./config:/config` - Path to create the MiniMusic Config

## Contributing

To contribute, see [contributing guidelines](CONTRIBUTING.md).
