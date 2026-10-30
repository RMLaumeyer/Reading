import unittest
import issue_designators as designation
import guide_order
import cbro_order


class DecimalCaptureTests(unittest.TestCase):
    def test_preserves_designator_without_float_conversion_or_identity_claim(self):
        for text in ('Original Sin (2014) #3.10', 'Original Sin #3.10 (2014)'):
            row = designation.decimal_issue(text)
            self.assertEqual(row['designator'], '3.10')
            self.assertEqual(row['series'], 'Original Sin')
            self.assertEqual(row['year'], 2014)
            self.assertFalse(row['identityEstablished'])
            self.assertFalse(row['membershipEstablished'])

    def test_does_not_guess_ranges_annotations_or_conflicting_years(self):
        for text in ('Original Sin #3.1-3.4', 'Original Sin #3',
                     'Original Sin #3.1 optional', 'Original Sin (2014) #3.1 (2015)',
                     'Original Sin #3.1 (9999)'):
            self.assertIsNone(designation.decimal_issue(text))

    def test_both_adapters_retain_decimal_as_unresolved_source_position(self):
        raw = '<h1>Example Reading Order</h1><p>Part 1: Event</p><p>Reading Order:</p><li>Original Sin (2014) #3.10</li>'
        paths = [guide_order.parse(raw, 'https://marvelguides.com/example-reading-order', ['Part 1: Event'], [])]
        raw = '<h1>Example</h1><button role="tab" aria-controls="single">Single Issues</button><div role="tabpanel" id="single"><p>Original Sin #3.10 (2014)</p></div>'
        paths.append(cbro_order.parse(raw, 'https://comicbookreadingorders.com/marvel/events/example-reading-order/'))
        for path in paths:
            self.assertEqual(path['orderedIssues'], [])
            self.assertEqual(len(path['sourceSequence']), 1)
            slot = path['sourceSequence'][0]
            self.assertIsNone(slot['issue'])
            self.assertEqual(slot['identityState'], 'unsupported')
            self.assertEqual(slot['unsupportedIssueDesignation']['designator'], '3.10')
            self.assertFalse(path['complete'])


if __name__ == '__main__':
    unittest.main()
