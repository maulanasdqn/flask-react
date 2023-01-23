let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  buildInputs = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.virtualenv
    pkgs.python310Packages.flask
    pkgs.python310Packages.click
    pkgs.python310Packages.cycler
    pkgs.python310Packages.colorama
    pkgs.python310Packages.greenlet
    pkgs.python310Packages.itsdangerous
    pkgs.python310Packages.joblib
    pkgs.python310Packages.kiwisolver
    pkgs.python310Packages.matplotlib
    pkgs.python310Packages.numpy
    pkgs.python310Packages.packaging
    pkgs.python310Packages.pandas
    pkgs.python310Packages.pyparsing
    pkgs.python310Packages.python-dateutil
    pkgs.python310Packages.pytz
    pkgs.python310Packages.scikit-learn
    pkgs.python310Packages.scipy
    pkgs.python310Packages.seaborn
    pkgs.python310Packages.six
    pkgs.python310Packages.sqlalchemy
    pkgs.python310Packages.flask_sqlalchemy
    pkgs.python310Packages.threadpoolctl
    pkgs.python310Packages.werkzeug
    pkgs.python310Packages.mariadb
    pkgs.python310Packages.mysqlclient
    pkgs.python310Packages.python-dotenv
  ];
  shellHook = ''
    export PIP_PREFIX=$(pwd)/_build/pip_packages
    export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
    export PATH="$PIP_PREFIX/bin:$PATH"
    unset SOURCE_DATE_EPOCH
  '';
}
