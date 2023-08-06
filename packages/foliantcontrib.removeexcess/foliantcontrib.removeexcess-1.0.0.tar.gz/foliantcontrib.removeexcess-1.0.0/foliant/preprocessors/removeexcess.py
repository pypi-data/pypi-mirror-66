'''
Preprocessor for Foliant documentation authoring tool.

Removes unneseccary Markdown files that are not mentioned in chapters.
'''

from pathlib import Path

from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('removeexcess')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def apply(self):
        self.logger.info('Applying preprocessor')

        def _recursive_process_chapters(chapters_subset):
            if isinstance(chapters_subset, dict):
                new_chapters_subset = {}
                for key, value in chapters_subset.items():
                    new_chapters_subset[key] = _recursive_process_chapters(value)

            elif isinstance(chapters_subset, list):
                new_chapters_subset = []
                for item in chapters_subset:
                    new_chapters_subset.append(_recursive_process_chapters(item))

            elif isinstance(chapters_subset, str):
                if chapters_subset.endswith('.md'):
                    chapter_file_path = (self.working_dir / chapters_subset).resolve()

                    self.logger.debug(f'Adding file to the list of mentioned in chapters: {chapter_file_path}')

                    chapters_files_paths.append(chapter_file_path)

                new_chapters_subset = chapters_subset

            else:
                new_chapters_subset = chapters_subset

            return new_chapters_subset

        chapters_files_paths = []

        _recursive_process_chapters(self.config.get('chapters', []))

        self.logger.debug(f'List of files mentioned in chapters: {chapters_files_paths}')

        for markdown_file_path in self.working_dir.rglob('*.md'):
            markdown_file_path = markdown_file_path.resolve()

            self.logger.debug(f'Checking if the file is mentioned in chapters: {markdown_file_path}')

            if markdown_file_path in chapters_files_paths:
                self.logger.debug('Mentioned, keeping')

            else:
                self.logger.debug('Not mentioned, deleting')

                markdown_file_path.unlink()

        self.logger.info('Preprocessor applied')
