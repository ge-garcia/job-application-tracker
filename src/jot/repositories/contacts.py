from jot.models import ContactForm, ContactNotesForm, ContactRow
from jot.repositories.base import BaseRepository

_SELECT = """
    SELECT
        ct.contact_id,
        ct.company_id,
        ct.contact_name,
        ct.email,
        ct.phone,
        ct.title,
        ct.linkedin_url,
        ct.notes,
        c.company_name
    FROM contacts ct
    JOIN companies c ON c.company_id = ct.company_id
"""


class ContactRepository(BaseRepository):
    """Data access layer for the contacts table"""

    def list_all(self, search: str | None = None) -> list[ContactRow]:
        """Returns all contacts ordered alphabetically, optionally searching by name or email"""
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            sql = f"""
                {_SELECT}
                WHERE ct.contact_name LIKE %s OR ct.email LIKE %s
                ORDER BY ct.contact_name ASC, ct.contact_id ASC
            """
            self.cursor.execute(sql, (pattern, pattern))
        else:
            sql = f"""
                {_SELECT}
                ORDER BY ct.contact_name ASC, ct.contact_id ASC
            """
            self.cursor.execute(sql)

        return self._fetch_all(ContactRow)

    def get_by_id(self, contact_id: int) -> ContactRow | None:
        """Fetches a single contact by primary key, or None if not found"""
        sql = f"""
            {_SELECT}
            WHERE ct.contact_id = %s
        """
        self.cursor.execute(sql, (contact_id,))
        return self._fetch_one(ContactRow)

    def create(self, data: ContactForm) -> int | None:
        """Inserts a new contact and returns its generated contact_id"""
        params = data.to_params()
        sql = """
            INSERT INTO contacts (
                company_id,
                contact_name,
                email,
                phone,
                title,
                linkedin_url,
                notes
            ) VALUES (
                %(company_id)s,
                %(contact_name)s,
                %(email)s,
                %(phone)s,
                %(title)s,
                %(linkedin_url)s,
                %(notes)s
            )
        """
        self.cursor.execute(sql, params)
        return self.cursor.lastrowid

    def update(self, contact_id: int, data: ContactForm) -> bool:
        """Updates all editable fields on a contact and returns True if the row changed"""
        params = data.to_params()
        params["contact_id"] = contact_id
        sql = """
            UPDATE contacts
            SET company_id = %(company_id)s,
                contact_name = %(contact_name)s,
                email = %(email)s,
                phone = %(phone)s,
                title = %(title)s,
                linkedin_url = %(linkedin_url)s,
                notes = %(notes)s
            WHERE contact_id = %(contact_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def update_notes(self, contact_id: int, data: ContactNotesForm) -> bool:
        """Updates only the notes column for a contact, and returns True if the row changed"""
        params = data.to_params()
        params["contact_id"] = contact_id
        sql = """
            UPDATE contacts
            SET notes = %(notes)s
            WHERE contact_id = %(contact_id)s
        """
        self.cursor.execute(sql, params)
        return self.cursor.rowcount > 0

    def delete(self, contact_id: int) -> bool:
        """Deletes a contact by primary key"""
        sql = "DELETE FROM contacts WHERE contact_id = %s"
        self.cursor.execute(sql, (contact_id,))
        return self.cursor.rowcount > 0
