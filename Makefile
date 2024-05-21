
# Install all python library dependencies
setup:
	poetry install

make-data:

	poetry run python src/make_data/main.py
	 # ****** Finished generating data ******

	# Then pretty format the index
	bash ./scripts/upload_index_to_s3.sh
