# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfjeeves',
 'tfjeeves.callbacks',
 'tfjeeves.core',
 'tfjeeves.losses',
 'tfjeeves.models',
 'tfjeeves.models.metric',
 'tfjeeves.models.regression',
 'tfjeeves.models.triplet',
 'tfjeeves.plotting',
 'tfjeeves.tests',
 'tfjeeves.triplet',
 'tfjeeves.utils']

package_data = \
{'': ['*'],
 'tfjeeves.tests': ['fixtures/presize-output/categoryA/subcategoryA/subsubcategoryA/*',
                    'fixtures/presize-output/categoryA/subcategoryA/subsubcategoryB/*',
                    'fixtures/presize-output/categoryA/subcategoryB/subsubcategoryC/*',
                    'fixtures/presize-output/categoryA/subcategoryB/subsubcategoryD/*',
                    'fixtures/presize-output/categoryB/subcategoryA/subsubcategoryA/*',
                    'fixtures/presize-output/categoryB/subcategoryA/subsubcategoryB/*',
                    'fixtures/presize-output/categoryB/subcategoryB/subsubcategoryC/*',
                    'fixtures/presize-output/categoryB/subcategoryB/subsubcategoryD/*',
                    'fixtures/presize/categoryA/subcategoryA/subsubcategoryA/*',
                    'fixtures/presize/categoryA/subcategoryA/subsubcategoryB/*',
                    'fixtures/presize/categoryA/subcategoryB/subsubcategoryC/*',
                    'fixtures/presize/categoryA/subcategoryB/subsubcategoryD/*',
                    'fixtures/presize/categoryB/subcategoryA/subsubcategoryA/*',
                    'fixtures/presize/categoryB/subcategoryA/subsubcategoryB/*',
                    'fixtures/presize/categoryB/subcategoryB/subsubcategoryC/*',
                    'fixtures/presize/categoryB/subcategoryB/subsubcategoryD/*']}

install_requires = \
['attrdict>=2.0.1,<3.0.0',
 'black>=19.10b0,<20.0',
 'boto3>=1.12.33,<2.0.0',
 'boto>=2.49.0,<3.0.0',
 'click>=7.0,<8.0',
 'efficientnet>=1.1.0,<2.0.0',
 'h5py>=2.10.0,<3.0.0',
 'hyperdash>=0.15.3,<0.16.0',
 'joblib>=0.14.1,<0.15.0',
 'loguru>=0.4.0,<0.5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'pandas>=1.0.0,<2.0.0',
 'pillow==7.1.1',
 'plot_keras_history>=1.1.23,<2.0.0',
 'plotnine>=0.6.0,<0.7.0',
 'py3nvml>=0.2.5,<0.3.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scikit-learn>=0.22.2,<0.23.0',
 'tensordash>=0.1.0,<0.2.0',
 'tensorflow-estimator==2.1.0',
 'tensorflow==2.1.0',
 'tf-explain>=0.2.1,<0.3.0',
 'tqdm>=4.41.1,<5.0.0']

entry_points = \
{'console_scripts': ['fix = scripts:fix',
                     'generate_triplets = scripts:generate_triplets',
                     'generate_vista_triplets = '
                     'scripts:generate_vista_triplets',
                     'grad_cam = scripts:grad_cam',
                     'train = train:run',
                     'update_categories = scripts:update_categories']}

setup_kwargs = {
    'name': 'tfjeeves',
    'version': '0.2.6',
    'description': 'Utilities to help train models with tensorflow2 and keras',
    'long_description': "# tfjeeves\n\n`poetry run python train.py --config=configs/cifar10.py --data=/home/soumendra/data-zoo/classification/cifar10`\n\nhttps://flynn.gg/blog/software-best-practices-python-2019/\n\n```bash\npoetry run python train.py --config=configs/cifar10.py --data=~/data-zoo/classification/cifar10\n```\n\nGetting triplet list (df)\n\n```\nDATABASE_URL=postgresql://vista_api_live:4jzjS3USGnjLvXZrHrR4cyNh@vista-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com:5432/vista_api_live\nETL_DATABASE_URL=postgresql://etl_user:eCwTqY6h9DJeFwFyuyX4LcSF@etl-server-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com:5432/etldb\n\n```\n\n```\npsql -h etl-server-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com -p 5432 -U etl_user -d etldb\n\n\\copy (SELECT tot.catalog_id, tot.product_id, tot.master_name, tot.subcategory_name, tot.category_name, tot.image_id, sync.s3_path, sync.is_sizechart, sync.is_discarded  FROM (SELECT fc.catalog_id, fc.product_id, fc.master_name, fc.subcategory_name, fc.category_name, fvi.image_id FROM (SELECT catalog_id, UNNEST(product_ids) as product_id, master_name, subcategory_name, category_name FROM fact_catalogs AS fc WHERE catalog_product_count > 3) AS fc JOIN fact_visible_images AS fvi ON fvi.product_id = fc.product_id) AS tot JOIN synced_images AS sync ON sync.image_id = tot.image_id ORDER BY tot.catalog_id) to 'temp.csv' delimiter ',' csv header;\n```\n",
    'author': 'Soumendra Dhanee',
    'author_email': 'soumendra@gmail.com',
    'maintainer': 'Soumendra Dhanee',
    'maintainer_email': 'soumendra@gmail.com',
    'url': 'https://github.com/soumendra/tfjeeves',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.7.6',
}


setup(**setup_kwargs)
