import json

class InferenceEngine:
    """Forward chaining engine untuk Sistem Skripsi Assistant"""

    def __init__(self, rules_path='rules.json'):
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.knowledge = json.load(f)

    def forward_chain(self, jurusan, minat=None, metode=None):
        """Forward chaining: dari fakta (jurusan/minat/metode) tarik rekomendasi"""
        if jurusan not in self.knowledge['jurusan']:
            return {'error': 'Jurusan tidak ditemukan'}

        fakta = self.knowledge['jurusan'][jurusan]
        fired = []

        # Aturan 1: cocokkan jurusan
        fired.append(f"Jurusan = {jurusan}")
        topik = fakta['topik']
        metodologi = fakta['metodologi']

        # Aturan 2: filter minat (jika ada)
        if minat:
            minat_lower = minat.lower()
            topik_filtered = [t for t in topik if minat_lower in t.lower()]
            if topik_filtered:
                topik = topik_filtered
                fired.append(f"Minat '{minat}' cocok dengan topik")
            else:
                fired.append(f"Topik '{minat}' tidak ada — tampilkan semua topik jurusan")

        # Aturan 3: cocokkan atau rekomendasikan metodologi
        if metode:
            if metode == metodologi:
                fired.append(f"Metode {metode} sesuai dengan jurusan")
            else:
                fired.append(f"Metode {metode} tidak umum untuk jurusan ini — rekomendasi: {metodologi}")

        return {
            'jurusan': jurusan,
            'topik': topik,
            'metodologi': metodologi,
            'variabel': fakta['variabel'],
            'hipotesis': fakta['hipotesis'],
            'proses': fired,
            'jumlah_aturan_terpicu': len(fired)
        }

    def get_jurusan_list(self):
        return list(self.knowledge['jurusan'].keys())
