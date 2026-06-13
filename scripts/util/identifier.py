import re

class Identifier:
	# I dont care about optimization in this project
	NAMESPACE_PATTERN = re.compile(r"^[a-z0-9_\-\.]+$")
	PATH_PATTERN = re.compile(r"^[a-z0-9_\-\./]+$")

	def __init__(self, path: str):
		if ":" in path: self.namespace, self.path = path.split(":", 1)
		else:
			self.namespace = "minecraft"
			self.path = path
		self.path = self.path.replace("\\", "/")

		if not self.NAMESPACE_PATTERN.match(self.namespace): raise ValueError(
			f"Invalid Identifier: Namespace '{self.namespace}' mengandung karakter ilegal! "
			f"Hanya boleh menggunakan huruf kecil, angka, '_', '-', dan '.'."
		)

		if not self.PATH_PATTERN.match(self.path): raise ValueError(
			f"Invalid Identifier: Path '{self.path}' mengandung karakter ilegal! "
			f"Hanya boleh menggunakan huruf kecil, angka, '_', '-', '.', dan '/'."
		)

	def __str__(self) -> str:
		return f"{self.namespace}:{self.path}"

	def __repr__(self) -> str:
		return f"Identifier('{self.namespace}:{self.path}')"

	@property
	def is_vanilla(self) -> bool:
		return self.namespace == "minecraft"