
# Install all python library dependencies
setup:
	poetry install

create-data:

	poetry run python src/create_data/main.py
	 # ****** Finished generating data ******

	# Then pretty format the index
	bash ./scripts/upload_index_to_s3.sh
