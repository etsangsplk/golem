from datetime import datetime

from peewee import IntegrityError

import golem.model as m
from golem.testutils import DatabaseFixture, PEP8MixIn, TempDirFixture


class TestDatabase(TempDirFixture, PEP8MixIn):
    PEP8_FILES = ["golem/model.py"]

    def test_init(self):
        db = m.Database(self.path)
        self.assertFalse(db.db.is_closed())
        db.db.close()

    def test_schema_version(self):
        db = m.Database(self.path)
        self.assertEqual(db._get_user_version(), db.SCHEMA_VERSION)
        self.assertNotEqual(db.SCHEMA_VERSION, 0)

        db._set_user_version(0)
        self.assertEqual(db._get_user_version(), 0)
        db = m.Database(self.path)
        self.assertEqual(db._get_user_version(), db.SCHEMA_VERSION)
        db.db.close()


class TestPayment(DatabaseFixture):

    def test_default_fields(self):
        p = m.Payment()
        self.assertGreaterEqual(datetime.now(), p.created_date)
        self.assertGreaterEqual(datetime.now(), p.modified_date)

    def test_create(self):
        p = m.Payment(payee="DEF", subtask="xyz", value=5,
                    status=m.PaymentStatus.awaiting)
        self.assertEqual(p.save(force_insert=True), 1)

        with self.assertRaises(IntegrityError):
            m.Payment.create(payee="DEF", subtask="xyz", value=5,
                             status=m.PaymentStatus.awaiting)
        m.Payment.create(payee="DEF", subtask="xyz2", value=4,
                         status=m.PaymentStatus.confirmed)
        m.Payment.create(payee="DEF2", subtask="xyz4", value=5,
                         status=m.PaymentStatus.sent)

        self.assertEqual(3, len([payment for payment in m.Payment.select()]))

    def test_invalid_status(self):
        with self.assertRaises(TypeError):
            m.Payment.create(payee="XX", subtask="zz", value=5, status=1)

    def test_invalid_value_type(self):
        with self.assertRaises(TypeError):
            m.Payment.create(payee="XX", subtask="float", value=5.5,
                             status=m.PaymentStatus.sent)
        with self.assertRaises(TypeError):
            m.Payment.create(payee="XX", subtask="str", value="500",
                             status=m.PaymentStatus.sent)

    def test_payment_details(self):
        p1 = m.Payment(payee="me", subtask="T1000", value=123456)
        p2 = m.Payment(payee="you", subtask="T900", value=654321)
        self.assertNotEqual(p1.payee, p2.payee)
        self.assertNotEqual(p1.subtask, p2.subtask)
        self.assertNotEqual(p1.value, p2.value)
        self.assertEqual(p1.details, {})
        self.assertEqual(p1.details, p2.details)
        self.assertIsNot(p1.details, p2.details)
        p1.details['check'] = True
        self.assertTrue(p1.details['check'])
        self.assertNotIn('check', p2.details)

    def test_payment_big_value(self):
        value = 10000 * 10**18
        assert value > 2**64
        m.Payment.create(payee="me", subtask="T1000", value=value,
                         status=m.PaymentStatus.sent)


class TestReceivedPayment(DatabaseFixture):

    def test_default_fields(self):
        r = m.ReceivedPayment()
        self.assertGreaterEqual(datetime.now(), r.created_date)
        self.assertGreaterEqual(datetime.now(), r.modified_date)

    def test_create(self):
        r = m.ReceivedPayment(from_node_id="DEF", task="xyz", val=4,
                              expected_val=3131, state="SOMESTATE")
        self.assertEquals(r.save(force_insert=True), 1)
        with self.assertRaises(IntegrityError):
            m.ReceivedPayment.create(from_node_id="DEF", task="xyz", val=5,
                                     expected_val=3132, state="SOMESTATEX")
        m.ReceivedPayment.create(from_node_id="DEF", task="xyz2", val=5,
                                 expected_val=3132, state="SOMESTATEX")
        m.ReceivedPayment.create(from_node_id="DEF2", task="xyz", val=5,
                                 expected_val=3132, state="SOMESTATEX")

        self.assertEqual(3, len([payment
                                 for payment in m.ReceivedPayment.select()]))


class TestLocalRank(DatabaseFixture):

    def test_default_fields(self):
        r = m.LocalRank()
        self.assertGreaterEqual(datetime.now(), r.created_date)
        self.assertGreaterEqual(datetime.now(), r.modified_date)
        self.assertEqual(0, r.positive_computed)
        self.assertEqual(0, r.negative_computed)
        self.assertEqual(0, r.wrong_computed)
        self.assertEqual(0, r.positive_requested)
        self.assertEqual(0, r.negative_requested)
        self.assertEqual(0, r.positive_payment)
        self.assertEqual(0, r.negative_payment)
        self.assertEqual(0, r.positive_resource)
        self.assertEqual(0, r.negative_resource)


class TestGlobalRank(DatabaseFixture):

    def test_default_fields(self):
        r = m.GlobalRank()
        self.assertGreaterEqual(datetime.now(), r.created_date)
        self.assertGreaterEqual(datetime.now(), r.modified_date)
        self.assertEqual(m.NEUTRAL_TRUST, r.requesting_trust_value)
        self.assertEqual(m.NEUTRAL_TRUST, r.computing_trust_value)
        self.assertEqual(0, r.gossip_weight_computing)
        self.assertEqual(0, r.gossip_weight_requesting)


class TestNeighbourRank(DatabaseFixture):

    def test_default_fields(self):
        r = m.NeighbourLocRank()
        self.assertGreaterEqual(datetime.now(), r.created_date)
        self.assertGreaterEqual(datetime.now(), r.modified_date)
        self.assertEqual(m.NEUTRAL_TRUST, r.requesting_trust_value)
        self.assertEqual(m.NEUTRAL_TRUST, r.computing_trust_value)


class TestTaskPreset(DatabaseFixture):
    def test_default_fields(self):
        tp = m.TaskPreset()
        assert datetime.now() >= tp.created_date
        assert datetime.now() >= tp.modified_date


class TestPerformance(DatabaseFixture):
    def test_default_fields(self):
        perf = m.Performance()
        assert datetime.now() >= perf.created_date
        assert datetime.now() >= perf.modified_date
        assert perf.value == 0.0

    def test_constraints(self):
        perf = m.Performance()
        # environment_id can't be null
        with self.assertRaises(IntegrityError):
            perf.save()

        perf.environment_id = "ENV1"
        perf.save()

        perf = m.Performance(environment_id="ENV2", value=138.18)
        perf.save()

        env1 = m.Performance.get(m.Performance.environment_id == "ENV1")
        assert env1.value == 0.0
        env2 = m.Performance.get(m.Performance.environment_id == "ENV2")
        assert env2.value == 138.18

        # environment_id must be unique
        perf3 = m.Performance(environment_id="ENV1", value=1472.11)
        with self.assertRaises(IntegrityError):
            perf3.save()

        # value doesn't have to be unique
        perf3 = m.Performance(environment_id="ENV3", value=138.18)
        perf3.save()
