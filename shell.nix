{ pkgs ? import <nixpkgs> { } }:
let
  unstable = import <nixos-unstable> {
    config = {allowUnfree = true; };
  };
in
pkgs.mkShell {
  buildInputs = [
    unstable.python310Packages.discordpy
    pkgs.python310Packages.pyyaml
  ];
}
