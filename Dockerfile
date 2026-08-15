FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ------------------------------------------------------------
# System dependencies
# ------------------------------------------------------------

RUN apt-get update && apt-get install -y --no-install-recommends \
    zsh \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    unzip \
    cmake \
    ninja-build \
    clang \
    clangd \
    clang-format \
    git \
    curl \
    wget \
    nodejs \
    npm \
    ripgrep \
    fd-find \
    libxcb1 \
    libx11-6 \
    libx11-xcb1 \
    libxext6 \
    libxrender1 \
    libxcb-render0 \
    libxcb-shm0 \
    libxcb-xfixes0 \
    libxcb-randr0 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-icccm4 \
    libxcb-sync1 \
    libxcb-util1 \
    libxcb-xkb1 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libice6 \
    fontconfig \
    fonts-dejavu \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Oh My Zsh
# ------------------------------------------------------------

RUN git clone \
    --depth=1 \
    https://github.com/ohmyzsh/ohmyzsh.git \
    /root/.oh-my-zsh

# ------------------------------------------------------------
# Zsh plugins
# ------------------------------------------------------------

RUN git clone \
    --depth=1 \
    https://github.com/zsh-users/zsh-autosuggestions.git \
    /root/.oh-my-zsh/custom/plugins/zsh-autosuggestions

RUN git clone \
    --depth=1 \
    https://github.com/zsh-users/zsh-syntax-highlighting.git \
    /root/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting

# ------------------------------------------------------------
# Zsh configuration
# ------------------------------------------------------------

RUN printf '%s\n' \
    'export ZSH="$HOME/.oh-my-zsh"' \
    'ZSH_THEME=""' \
    '' \
    'plugins=(' \
    '    git' \
    '    zsh-autosuggestions' \
    '    zsh-syntax-highlighting' \
    ')' \
    '' \
    'source "$ZSH/oh-my-zsh.sh"' \
    '' \
    'autoload -U colors && colors' \
    'setopt PROMPT_SUBST' \
    '' \
    'PROMPT="%(?:%{$fg_bold[green]%}:%{$fg_bold[red]%})%{$fg[cyan]%}%n@%m %~%{$reset_color%} "' \
    '' \
    "alias l='ls -lah'" \
    "alias szh='source ~/.zshrc'" \
    > /root/.zshrc

# ------------------------------------------------------------
# Python virtual environment
# ------------------------------------------------------------

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# ------------------------------------------------------------
# Python dependencies
# ------------------------------------------------------------

RUN pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio

RUN pip install --no-cache-dir \
    opencv-python

RUN pip install --no-cache-dir \
    ultralytics

RUN pip install --no-cache-dir \
    black

RUN pip install --no-cache-dir \
    numpy \
    tqdm \
    scikit-learn

# ------------------------------------------------------------
# Workspace
# ------------------------------------------------------------

WORKDIR /workspace

CMD ["zsh"]