class Validator:
    """Validasi input user untuk Sistem Skripsi Assistant"""

    REQUIRED_FIELDS = ['jurusan']

    def validate(self, data):
        """Validasi data input, return (is_valid, errors)"""
        errors = []

        for field in self.REQUIRED_FIELDS:
            if field not in data or not data[field]:
                errors.append(f"Field '{field}' wajib diisi")

        if 'jurusan' in data and data['jurusan'] not in self._get_jurusan():
            errors.append(f"Jurusan '{data['jurusan']}' tidak valid")

        if 'metode' in data and data['metode'] not in ('kuantitatif', 'kualitatif', 'mixed'):
            errors.append("Metode harus: kuantitatif, kualitatif, atau mixed")

        return (len(errors) == 0, errors)

    def _get_jurusan(self):
        import json
        with open('rules.json', 'r', encoding='utf-8') as f:
            return list(json.load(f)['jurusan'].keys())
