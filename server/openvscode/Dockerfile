FROM gitpod/openvscode-server:latest

# to get permissions to install packages and such
USER root 

# the installation process for software needed
RUN apt update && apt install -y python3.10 python3-pip

# to restore permissions for the web interface
USER openvscode-server 

RUN pip install fastapi "uvicorn[standard]"

# Install vscode extensions
ENV OPENVSCODE_SERVER_ROOT="/home/.openvscode-server"
ENV OPENVSCODE="${OPENVSCODE_SERVER_ROOT}/bin/openvscode-server"

SHELL ["/bin/bash", "-c"]
RUN \
    # Direct download links to external .vsix not available on https://open-vsx.org/
    # The two links here are just used as example, they are actually available on https://open-vsx.org/
    urls=(\
    https://github.com/rust-lang/rust-analyzer/releases/download/2022-12-26/rust-analyzer-linux-x64.vsix \
    https://github.com/VSCodeVim/Vim/releases/download/v1.24.3/vim-1.24.3.vsix \
    )\
    # Create a tmp dir for downloading
    && tdir=/tmp/exts && mkdir -p "${tdir}" && cd "${tdir}" \
    # Download via wget from $urls array.
    && wget "${urls[@]}" && \
    # List the extensions in this array
    exts=(\
    # From https://open-vsx.org/ registry directly
    gitpod.gitpod-theme \
    # From filesystem, .vsix that we downloaded (using bash wildcard '*')
    "${tdir}"/* \
    )\
    # Install the $exts
    && for ext in "${exts[@]}"; do ${OPENVSCODE} --install-extension "${ext}"; done

ENV PATH=/home/workspace/.local/bin:$PATH