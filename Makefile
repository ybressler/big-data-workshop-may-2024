
# Install all python library dependencies
setup:
	poetry install

quest-1:

	poetry run python src/quest_1/quest_1.py
	 # ****** Finished ingesting data ******

	# Then pretty format the index
	bash ./scripts/upload_index_to_s3.sh


quest-2:

	poetry run python src/quest_1/quest_2.py
