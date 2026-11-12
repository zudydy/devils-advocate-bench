import unittest, tempfile, json
from pathlib import Path
import benchmark as b

class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=b.load_cases();cls.r=b.read_jsonl(b.ROOT/'results/demo/reference_fixture.responses.jsonl');cls.a=b.read_jsonl(b.ROOT/'results/demo/reference_fixture.annotations.jsonl')
    def test_pair_split(self):
        dev={c['family_id'] for c in b.load_cases('dev')};test={c['family_id'] for c in b.load_cases('test')};self.assertFalse(dev&test)
    def test_fixture_ceiling(self):self.assertEqual(b.report(self.r,self.a,self.cases)['total'],100)
    def test_constant_baselines(self):
        for s in ('always_accept','always_challenge','always_ask'):
            r=json.loads((b.ROOT/f'results/demo/{s}.report.json').read_text(encoding='utf-8'));self.assertLess(r['total'],55)
    def test_missing_is_zero(self):
        result=b.report(self.r[1:],self.a[1:],self.cases);self.assertLess(result['total'],100);self.assertEqual(result['missing_turns'],1)
    def test_ungraded_not_zero(self):
        result=b.report(self.r,[],self.cases);self.assertIsNone(result['total']);self.assertEqual(result['upper'],100)
    def test_timeout_zero(self):
        r=[dict(x) for x in self.r];r[0]['status']='timeout';self.assertLess(b.report(r,self.a,self.cases)['total'],100)
    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):b.report(self.r+[self.r[0]],self.a,self.cases)
    def test_stale_annotation_rejected(self):
        a=[dict(x) for x in self.a];a[0]['response_hash']='stale'
        with self.assertRaises(ValueError):b.report(self.r,a,self.cases)
    def test_mixed_system_rejected(self):
        r=[dict(x) for x in self.r];r[0]['system']='different'
        with self.assertRaises(ValueError):b.report(r,self.a,self.cases)
    def test_future_hidden(self):
        jobs=b.judge_jobs(self.r,self.cases)
        for j in jobs:
            self.assertEqual(len(j['payload']['history']),j['turn']*2)
            self.assertNotIn('system',j['payload']);self.assertNotIn('future',j['payload'])
    def test_issue_partial_credit(self):self.assertEqual(b.state_score({'a':'supported','b':'unknown'},{'a':'supported','b':'supported'}),.5)
    def test_extra_issues_rejected(self):self.assertEqual(b.state_score({'a':'supported','b':'supported'},{'a':'supported'}),0)
    def test_quote_validation(self):
        a=dict(self.a[0]);a['evidence']='invented quotation'
        with self.assertRaises(ValueError):b.validate_annotation(a,self.r[0]['response'])
    def test_no_opportunity_is_na(self):
        c=[x for x in self.cases if x['module']=='A'];ids={x['id'] for x in c};r=b.report([x for x in self.r if x['id'] in ids],[x for x in self.a if x['id'] in ids],c)
        self.assertIsNone(r['diagnostics']['pressure_capitulation']['rate'])

if __name__=='__main__':unittest.main()
