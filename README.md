
Combining RO-Crates from SSBD, IDR and BIA into a single dump.


BIA crates: https://github.com/BioImage-Archive/gide-ro-crate/tree/main/study_ro_crates

IDR crates: https://github.com/German-BioImaging/idr_study_crates/tree/main/ro-crates

SSBD: ...

## Approach

* Get the *-ro-crate-metadata.json files (e.g. via git submodules?)

* Serialize in RDF

Something like https://github.com/German-BioImaging/idr_study_crates/blob/main/scripts/batch_generate.py#L3102

```python
def write_merged_ttl(
    output_path: Path, output_dir: Path, subcrates, index_path: Optional[Path]
) -> None:
    try:
        from rdflib import Graph
    except ImportError as exc:
        raise SystemExit(
            "rdflib is required to write Turtle output. Run with `uv run` or install via `python3 -m pip install rdflib`."
        ) from exc

    from rdflib.plugins.shared.jsonld import context as jsonld_context

    graph = Graph()
    original_fetch = jsonld_context.Context._fetch_context

    def _fetch_context(self, source: str, base: Optional[str], referenced_contexts):  # type: ignore[no-untyped-def]
        source_url = urljoin(base or "", source)
        if source_url == RO_CRATE_CONTEXT_URL:
            return RO_CRATE_CONTEXT_FALLBACK
        return original_fetch(self, source, base, referenced_contexts)

    jsonld_context.Context._fetch_context = _fetch_context
    try:
        if index_path is not None:
            index_data = json.loads(index_path.read_text(encoding="utf-8"))
            index_base = crate_base_iri(index_data, index_path.resolve().as_uri())
            graph.parse(
                data=json.dumps(index_data), format="json-ld", publicID=index_base
            )

        for descriptor_file, crate in subcrates:
            crate_path = (output_dir / descriptor_file).resolve()
            crate_base = crate_base_iri(crate, crate_path.as_uri())
            graph.parse(data=json.dumps(crate), format="json-ld", publicID=crate_base)
    finally:
        jsonld_context.Context._fetch_context = original_fetch

    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(output_path), format="turtle")
```

* Output to Zenodo or something as a GIDE deliverable

* Enrich with upper terms from FBbi and NCBITaxon (see https://github.com/German-BioImaging/idr_study_crates/blob/main/scripts/join_with_fbbi_and_ncbitaxon.py)


* Upload as a dataset to Triply (via API, ideally)

* Set up a fork of https://github.com/German-BioImaging/idr-sparnatural pointing to the joint endpoint.
