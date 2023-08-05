"""
.. autoclass:: articlequality.Extractor
    :members:

.. autoclass:: articlequality.TemplateExtractor
    :members:
    :inherited-members:
"""

import logging
import sys
import traceback

import mwparserfromhell as mwp
import mwreverts

logger = logging.getLogger(__name__)


class Extractor:
    """
    Implements an labeling event extraction strategy.

    :Parameters:
        name : `str`
            A name for the extraction strategy
        doc : `str`
            Documentation describing the extraction strategy
        namespace : `iterable`(`int`)
            A set of namespaces that will be considered when performin an
            extraction
    """
    def __init__(self, name, doc, namespaces):
        self.__name__ = str(name)
        self.__doc__ = str(doc)
        self.namespaces = set(namespaces)

    def extract(self, page, verbose=False):
        """
        Processes an :class:`mwxml.Page` and returns a generator of
        first-observations of a project/label pair.

        :Parameters:
            page : :class:`mwxml.Page`
                Page to process
            verbose : `bool`
                print dots to stderr

        """
        if page.namespace not in self.namespaces:
            pass
        else:
            if verbose:
                sys.stderr.write("\n{0}: ".format(page.title))
                sys.stderr.flush()

            labelings = {}
            last_labels = set()
            detector = mwreverts.Detector()

            # Process all of the revisions looking for new class labels
            for revision in page:

                revert = detector.process(revision.sha1, revision.id)

                try:
                    revision_text = revision.text or ""
                    project_labels = set(pl for pl in
                                         self.extract_labels(revision_text))
                except:
                    logger.warning("Could not extract labels from text:")
                    logger.warning(traceback.format_exc())
                    continue

                if revert is not None:
                    # This revision is a revert.
                    for rev_id in revert.reverteds:
                        if rev_id in labelings:
                            for lab in labelings[rev_id]:
                                lab['reverted'] = True

                    if revert.reverted_to in labelings:
                        for lab in labelings[revert.reverted_to]:
                            lab['reverted'] = False

                    if verbose:
                        sys.stderr.write("r")
                        sys.stderr.flush()
                else:
                    # This revision is not a revert.  Get the new labels
                    new_labels = project_labels - last_labels

                    # Log some verbose stuff
                    if verbose:
                        if len(new_labels) > 0:
                            sys.stderr.write("l")
                            sys.stderr.flush()
                        else:
                            sys.stderr.write(".")
                            sys.stderr.flush()

                    # Update lookup of rev_ids that affect labelings
                    if len(new_labels) > 0:
                        labelings[revision.id] = [
                            {'rev_id': revision.id,
                             'project': project,
                             'wp10': wp10,
                             'timestamp': revision.timestamp,
                             'reverted': False}
                            for project, wp10 in new_labels
                        ]

                # Update state so we make an appropriate comparison next time
                last_labels = project_labels

            # Find first labelings and filter out reverted labelings
            first_observations = {}
            for observations in labelings.values():
                for ob in observations:
                    if ob['reverted']:
                        continue
                    pair = (ob['project'], ob['wp10'])
                    if pair in first_observations:
                        if ob['timestamp'] < \
                           first_observations[pair]['timestamp']:
                            first_observations[pair] = ob
                    else:
                        first_observations[pair] = ob

            # All cleaned up.  Yield what we've got.
            for ob in first_observations.values():
                yield ob

    def extract_labels(self, text):
        raise NotImplementedError()


class TemplateExtractor(Extractor):
    """
    Implements a template-based extraction strategy based on a `from_template`
    function that takes a template and returns a (project, label) pair.

    :Parameters:
        from_template : `func`
            A function that takes a template and returns a (project, label)
            pair
    """
    def __init__(self, *args, from_template, **kwargs):
        self.from_template = from_template

        if 'filter_text' in kwargs:
            self.filter_text = kwargs.get('filter_text')
            kwargs.pop('filter_text', None)

        super().__init__(*args, **kwargs)

    def extract_labels(self, text):
        """
        Extracts a set of labels for a version of text by parsing templates.

        :Parameters:
            text : `str`
                Wikitext markup to extract labels from

        :Returns:
            An iterator over (project, label) pairs
        """
        # filter_text is an initial fast pass to weed out wikitext that
        # can't contain the template (eg. because the template name
        # never appears)
        if hasattr(self, 'filter_text'):
            if not self.filter_text(text):
                return

        parsed_text = mwp.parse(text)
        templates = parsed_text.filter_templates()
        for template in templates:

            yield from self.from_template(template)
