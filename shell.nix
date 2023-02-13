{ pkgs ? import <nixpkgs> { } }:
pkgs.mkShell {
  buildInputs = [
    pkgs.python310Packages.discordpy
    pkgs.python310Packages.pyyaml
  ];
}
