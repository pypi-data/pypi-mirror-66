""" Core definition of a Materials Document """
from typing import List, Dict, ClassVar, Union, Optional
from functools import partial
from datetime import datetime

from pydantic import BaseModel, Field, create_model

from pymatgen.analysis.magnetism import Ordering, CollinearMagneticStructureAnalyzer

from emmet.stubs import Structure
from emmet.core.structure import StructureMetadata


class PropertyOrigin(BaseModel):
    """
    Provenance document for the origin of properties in a material document
    """

    name: str = Field(..., description="The materials document property")
    task_type: str = Field(
        ..., description="The original calculation type this propeprty comes from"
    )
    task_id: str = Field(..., description="The calculation ID this property comes from")
    last_updated: datetime = Field(
        ..., description="The timestamp when this calculation was last updated"
    )


class MaterialsDoc(StructureMetadata):
    """
    Definition for a full Materials Document
    Subsections can be defined by other builders
    """

    structure: Structure = Field(
        None, description="The best structure for this material"
    )

    ordering: Ordering = Field(None, description="Magnetic Ordering for this structure")

    initial_structures: List[Structure] = Field(
        None,
        description="Initial structures used in the DFT optimizations corresponding to this material",
    )

    task_ids: List[str] = Field(
        None,
        title="Calculation IDs",
        description="List of Calculations IDs used to make this Materials Document",
    )

    deprecated_tasks: List[str] = Field(None, title="Deprecated Tasks")

    deprecated: bool = Field(
        None,
        description="Whether this materials document is deprecated due to a lack of high enough quality calculation.",
    )

    # Only material_id is required for all documents
    material_id: str = Field(
        ...,
        description="The ID of this material, used as a universal reference across proeprty documents."
        "This comes in the form: mp-******",
    )

    last_updated: datetime = Field(
        None,
        description="Timestamp for the most recent calculation for this Material document",
    )
    created_at: datetime = Field(
        None,
        description="Timestamp for the first calculation for this Material document",
    )
    calc_types: Dict[str, str] = Field(
        None,
        description="Calculation types for all the calculations that make up this material",
    )

    origins: List[PropertyOrigin] = Field(
        None, description="Dictionary for tracking the provenance of properties"
    )

    warnings: List[str] = Field(
        None, description="Any warnings related to this material"
    )

    sandboxes: List[str] = Field(
        None,
        description="List of sandboxes this material belongs to."
        " Sandboxes provide a way of controlling access to materials."
        " No sandbox means this materials is openly visible",
    )

    @staticmethod
    def from_structure(  # type: ignore[override]
        structure: Structure,
        material_id: str,
        fields: Optional[List[str]] = None,
        **kwargs
    ) -> "MaterialsDoc":
        """
        Builds a materials document using the minimal amount of information
        """
        meta = StructureMetadata.from_structure(structure, fields=fields)
        ordering = CollinearMagneticStructureAnalyzer(structure).ordering
        kwargs.update(**meta.dict())

        if "last_updated" not in kwargs:
            kwargs["last_updated"] = datetime.utcnow()

        if "created_at" not in kwargs:
            kwargs["created_at"] = datetime.utcnow()

        return MaterialsDoc(
            structure=structure, material_id=material_id, ordering=ordering, **kwargs
        )
