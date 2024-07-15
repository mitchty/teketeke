{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    ollama.url = "github:abysssol/ollama-flake";
    #ollama.inputs.nixpkgs.follows = "nixpkgs"; # this could break the build unless using unstable nixpkgs

    devshell.url = "github:numtide/devshell";
    flake-utils.url = "github:numtide/flake-utils";

    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs =
    { self
    , flake-utils
    , devshell
    , nixpkgs
    , ollama
    , ...
    }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShells.default =
        let
          pkgs = import nixpkgs {
            inherit system;

            overlays = [ devshell.overlays.default ];
          };
          pythonPackages = p: with p; [
            numpy
            pypdf
            langchain
            langchain-community
            chromadb
            pytest
            boto3
          ];
        in
        pkgs.devshell.mkShell {
          imports = [ (pkgs.devshell.importTOML ./devshell.toml) ];
          packages = with pkgs; [
            # In case there is another ollama, avoid a collision in
            # the derivation.
            (pkgs.lib.hiPrio ollama.packages.${system}.rocm)
            (pkgs.python311.withPackages pythonPackages)
          ];
        };
    });
  # # to access the rocm package of the ollama flake:
  # ollama-rocm = ollama.packages.${system}.rocm;
  # #ollama-rocm = inputs'.ollama.packages.rocm; # with flake-parts

  # # you can override package inputs like with nixpkgs
  # ollama-cuda = ollama.packages.${system}.cuda.override { cudaGcc = pkgs.gcc11; };
}
