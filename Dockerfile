# Generated by Neurodocker and Reproenv.

FROM ubuntu:22.04
RUN apt-get update -qq \
           && apt-get install -y -q --no-install-recommends \
                  ca-certificates \
                  curl \
                  gcc \
                  git \
                  gnupg2 \
                  pip \
                  python3 \
                  software-properties-common \
           && rm -rf /var/lib/apt/lists/*
RUN apt-key adv --fetch-keys https://apt.sr-research.com/SRResearch_key && add-apt-repository 'deb [arch=amd64] https://apt.sr-research.com SRResearch main'
RUN apt-get update -qq \
           && apt-get install -y -q --no-install-recommends \
                  eyelink-display-software \
           && rm -rf /var/lib/apt/lists/*
RUN mkdir /eye2bids
COPY [".", \
      "/eye2bids"]
WORKDIR /eye2bids
RUN pip install .[dev]

# Save specification to JSON.
RUN printf '{ \
  "pkg_manager": "apt", \
  "existing_users": [ \
    "root" \
  ], \
  "instructions": [ \
    { \
      "name": "from_", \
      "kwds": { \
        "base_image": "ubuntu:22.04" \
      } \
    }, \
    { \
      "name": "install", \
      "kwds": { \
        "pkgs": [ \
          "gnupg2", \
          "curl", \
          "gcc", \
          "ca-certificates", \
          "software-properties-common", \
          "python3", \
          "pip", \
          "git" \
        ], \
        "opts": null \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "apt-get update -qq \\\\\\n    && apt-get install -y -q --no-install-recommends \\\\\\n           ca-certificates \\\\\\n           curl \\\\\\n           gcc \\\\\\n           git \\\\\\n           gnupg2 \\\\\\n           pip \\\\\\n           python3 \\\\\\n           software-properties-common \\\\\\n    && rm -rf /var/lib/apt/lists/*" \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "apt-key adv --fetch-keys https://apt.sr-research.com/SRResearch_key && add-apt-repository '"'"'deb [arch=amd64] https://apt.sr-research.com SRResearch main'"'"'" \
      } \
    }, \
    { \
      "name": "install", \
      "kwds": { \
        "pkgs": [ \
          "eyelink-display-software" \
        ], \
        "opts": null \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "apt-get update -qq \\\\\\n    && apt-get install -y -q --no-install-recommends \\\\\\n           eyelink-display-software \\\\\\n    && rm -rf /var/lib/apt/lists/*" \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "mkdir /eye2bids" \
      } \
    }, \
    { \
      "name": "copy", \
      "kwds": { \
        "source": [ \
          ".", \
          "/eye2bids" \
        ], \
        "destination": "/eye2bids" \
      } \
    }, \
    { \
      "name": "workdir", \
      "kwds": { \
        "path": "/eye2bids" \
      } \
    }, \
    { \
      "name": "run", \
      "kwds": { \
        "command": "pip install .[dev]" \
      } \
    } \
  ] \
}' > /.reproenv.json
# End saving to specification to JSON.