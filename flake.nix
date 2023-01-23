{
  description = "Django with Nix";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    mach-nix.url = "mach-nix/3.5.0";
  };

  outputs = {self, nixpkgs, mach-nix }@inp:
    let
      l = nixpkgs.lib // builtins;
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forAllSystems = f: l.genAttrs supportedSystems
        (system: f system (import nixpkgs {inherit system;}));
    in
    {
      defaultPackage = forAllSystems (system: pkgs: mach-nix.lib."${system}".mkPython {
        requirements = builtins.readFile ./requirements.txt;
      });
    };
}

