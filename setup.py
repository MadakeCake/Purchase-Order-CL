from setuptools import setup, find_packages
from pathlib import Path

# Cargar README si existe (opcional, mejora la metadata del paquete)
readme_path = Path(__file__).with_name("README.md")
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="purchase_order_cl",
    version="0.0.1",
    description="Orden de Compra adaptada al sistema tributario chileno para Frappe/ERPNext",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tu Nombre / Empresa",
    author_email="you@example.com",
    packages=find_packages(include=["purchase_order_cl", "purchase_order_cl.*"]),
    include_package_data=True,
    install_requires=["frappe"],
    zip_safe=False,
    classifiers=[
        "Framework :: Frappe",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
