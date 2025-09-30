from setuptools import setup, find_packages

setup(
    name='purchase_order_cl',
    version='0.0.1',
    description='Orden de Compra adaptada al sistema tributario chileno',
    author='Tu Nombre / Empresa',
    author_email='you@example.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=("frappe",),
)
