# tfjeeves

`poetry run python train.py --config=configs/cifar10.py --data=/home/soumendra/data-zoo/classification/cifar10`

https://flynn.gg/blog/software-best-practices-python-2019/

```bash
poetry run python train.py --config=configs/cifar10.py --data=~/data-zoo/classification/cifar10
```

Getting triplet list (df)

```
DATABASE_URL=postgresql://vista_api_live:4jzjS3USGnjLvXZrHrR4cyNh@vista-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com:5432/vista_api_live
ETL_DATABASE_URL=postgresql://etl_user:eCwTqY6h9DJeFwFyuyX4LcSF@etl-server-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com:5432/etldb

```

```
psql -h etl-server-postgres.coaffiez9jim.ap-southeast-1.rds.amazonaws.com -p 5432 -U etl_user -d etldb

\copy (SELECT tot.catalog_id, tot.product_id, tot.master_name, tot.subcategory_name, tot.category_name, tot.image_id, sync.s3_path, sync.is_sizechart, sync.is_discarded  FROM (SELECT fc.catalog_id, fc.product_id, fc.master_name, fc.subcategory_name, fc.category_name, fvi.image_id FROM (SELECT catalog_id, UNNEST(product_ids) as product_id, master_name, subcategory_name, category_name FROM fact_catalogs AS fc WHERE catalog_product_count > 3) AS fc JOIN fact_visible_images AS fvi ON fvi.product_id = fc.product_id) AS tot JOIN synced_images AS sync ON sync.image_id = tot.image_id ORDER BY tot.catalog_id) to 'temp.csv' delimiter ',' csv header;
```
