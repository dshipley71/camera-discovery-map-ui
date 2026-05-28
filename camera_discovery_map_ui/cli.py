from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from camera_discovery_map_ui.agent import CameraDiscoveryMapAgent
from camera_discovery_map_ui.artifacts import load_artifacts
from camera_discovery_map_ui.bundle import build_bundle

app = typer.Typer(help="Build and inspect map UI bundles from camera-discovery artifacts.")
console = Console()


@app.command()
def inspect(input: Annotated[Path, typer.Option("--input", "-i", help="Artifact directory or ZIP file")]) -> None:
    """Inspect available known artifacts without building map outputs."""
    artifact_set = load_artifacts(input)
    bundle = build_bundle(artifact_set)
    table = Table(title="camera-discovery-map-ui artifact inspection")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("input_path", str(artifact_set.input_path))
    table.add_row("input_type", artifact_set.input_type)
    table.add_row("artifacts_found", ", ".join(artifact_set.artifacts_found) or "none")
    for key, value in bundle["summary"].items():
        if isinstance(value, dict):
            table.add_row(key, str(value))
        else:
            table.add_row(key, str(value))
    console.print(table)


@app.command()
def build(
    input: Annotated[Path, typer.Option("--input", "-i", help="Artifact directory or ZIP file")],
    output_dir: Annotated[Path, typer.Option("--output-dir", "-o", help="Directory for generated map UI artifacts")],
) -> None:
    """Build camera_map_bundle.json, camera_map.geojson, and map.html."""
    result = CameraDiscoveryMapAgent(input_path=input, output_dir=output_dir).run()
    summary = result.summary
    console.print("[bold green]Map UI artifacts written[/bold green]")
    console.print(f"records_total={summary['records_total']} mapped={summary['mapped_records']} unmapped={summary['unmapped_records']}")
    console.print(f"live={summary['live']} dead={summary['dead']} unknown={summary['unknown']}")
    console.print(f"bundle={result.bundle_path}")
    console.print(f"geojson={result.geojson_path}")
    console.print(f"map_html={result.map_html_path}")


if __name__ == "__main__":
    app()
