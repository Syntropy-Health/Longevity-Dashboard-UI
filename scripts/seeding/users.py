"""User seed data loading.

Loads demo patient users and admin user from seed data.
"""

from __future__ import annotations

from sqlmodel import Session, select

from longevity_clinic.app.data.model import User
from longevity_clinic.app.data.seed import get_all_demo_patients

from .base import SeedResult, print_section


def load_users(session: Session) -> SeedResult:
    """Load seed users and return mapping of external_id to db id.

    Uses DemoPatientSeed objects from seed/patients.py for consistency with config.
    The primary demo user (Sarah Chen) comes from DemoUserConfig.

    For demo purposes, Sarah Chen is created with BOTH patient and admin roles
    (as separate user records with different external_ids).

    Enforces ID order:
    1. Primary Patient (Sarah Chen) -> ID 1
    2. Admin User (Dr. Admin) -> ID 2
    3. Sarah Chen as Admin -> ID 3
    4. Secondary Patients -> ID 4+

    Returns:
        SeedResult with id_map of external_id -> database id
    """
    print_section("Loading users")
    result = SeedResult(name="users")

    # Get all demo patients
    all_patients = get_all_demo_patients()
    primary_patient = next(p for p in all_patients if p.is_primary)
    secondary_patients = [p for p in all_patients if not p.is_primary]

    def ensure_user(external_id, name, email, phone, role, is_primary=False, label=""):
        existing = session.exec(
            select(User).where(User.external_id == external_id)
        ).first()

        if existing:
            result.id_map[external_id] = existing.id
            result.skipped += 1
            marker = "★" if is_primary else "○"
            print(f"  {marker} Skipped (exists): {name} {label}(id={existing.id})")
            return existing

        user = User(
            external_id=external_id,
            name=name,
            email=email,
            phone=phone,
            role=role,
        )
        session.add(user)
        session.flush()  # Get the ID
        result.id_map[external_id] = user.id
        result.loaded += 1

        marker = "★" if is_primary else "✓"
        primary_label = " (PRIMARY)" if is_primary else ""
        print(f"  {marker} Created: {name} {label}{primary_label}(id={user.id})")
        return user

    # 1. Create Primary Patient (Sarah Chen) - ID 1
    ensure_user(
        primary_patient.external_id,
        primary_patient.name,
        primary_patient.email,
        primary_patient.phone,
        "patient",
        is_primary=True,
        label="[patient]",
    )

    # 2. Create Admin User (Dr. Admin) - ID 2
    ensure_user(
        "ADMIN001",
        "Dr. Admin",
        "admin@longevityclinic.com",
        None,
        "admin",
        label="[admin]",
    )

    # 3. Create Sarah Chen as Admin (for demo dual-role) - ID 3
    # Uses different external_id and email to maintain uniqueness
    admin_email = primary_patient.email.replace("@", "+admin@")
    ensure_user(
        f"{primary_patient.external_id}-ADMIN",
        primary_patient.name,
        admin_email,
        primary_patient.phone,
        "admin",
        label="[admin - dual role]",
    )

    # 4. Create Secondary Patients - ID 4+
    for patient in secondary_patients:
        ensure_user(
            patient.external_id,
            patient.name,
            patient.email,
            patient.phone,
            "patient",
            label="[patient]",
        )

    session.commit()
    print(f"  Total users: {len(result.id_map)}")
    return result
