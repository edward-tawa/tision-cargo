import uuid

from django.db import models

from trucks.models.truck_model import Truck


class TruckDocument(models.Model):
    """
    Stores critical tracking instances of legality compliance profiles (e.g., Registration cards, Permits, Border clearances).
    """

    class DocumentType(models.TextChoices):
        REGISTRATION = "REGISTRATION", "Vehicle Registration Certificate"
        ROADWORTHINESS = (
            "ROADWORTHINESS",
            "Roadworthiness/Inspection Safety Certificate",
        )
        TRANSIT_PERMIT = "TRANSIT_PERMIT", "Commercial Cross-Border Goods Permit"
        WEIGHT_CERTIFICATE = "WEIGHT_CERTIFICATE", "Certified Weight Bridge Slip"
        OTHER = "OTHER", "Supplementary Compliance Form"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    truck = models.ForeignKey(
        Truck, on_delete=models.CASCADE, related_name="compliance_documents"
    )

    document_type = models.CharField(max_length=30, choices=DocumentType.choices)
    document_number = models.CharField(
        max_length=100,
        help_text="The reference sequence identifier printed directly on the physical document asset.",
    )
    file_attachment = models.FileField(
        upload_to="trucks/compliance_vault/",
        help_text="Secure binary file location handling active cloud uploads safely.",
    )

    expiry_date = models.DateField(
        help_text="Calendar boundary warning systems calculations checkpoint tracking fields."
    )
    is_verified = models.BooleanField(
        default=False, help_text="System-level validation confirmation marker toggle."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Truck Document"
        verbose_name_plural = "Truck Documents"
        ordering = ["-expiry_date"]

        permissions = [
            ("can_add_truck_document", "Can add a new truck document"),
            ("can_update_truck_document", "Can update truck document details"),
            ("can_delete_truck_document", "Can delete a truck document"),
            ("can_verify_truck_document", "Can verify truck document compliance"),
            ("can_create_truck_document", "Can create a truck document"),
            ("can_read_truck_document", "Can read truck document details"),
        ]

    def __str__(self):
        return f"{self.get_document_type_display()} for Truck: {self.truck.license_plate_number}"
