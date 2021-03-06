#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector
from redisstat import RedisCollector

################################################################################


class TestRedisCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('RedisCollector', {
            'interval': '1',
            'databases': 1,
        })

        self.collector = RedisCollector(config, None)

    @patch.object(Collector, 'publish')
    def test_real_data(self, publish_mock):

        data_1 = {'pubsub_channels': 0,
                  'used_memory_peak_human': '700.71K',
                  'bgrewriteaof_in_progress': 0,
                  'connected_slaves': 0,
                  'uptime_in_days': 0,
                  'multiplexing_api': 'epoll',
                  'lru_clock': 954113,
                  'last_save_time': 1351718385,
                  'redis_version': '2.4.10',
                  'redis_git_sha1': 0,
                  'gcc_version': '4.4.6',
                  'connected_clients': 1,
                  'keyspace_misses': 0,
                  'used_memory': 726144,
                  'vm_enabled': 0,
                  'used_cpu_user_children': '0.00',
                  'used_memory_peak': 717528,
                  'role': 'master',
                  'total_commands_processed': 1,
                  'latest_fork_usec': 0,
                  'loading': 0,
                  'used_memory_rss': 7254016,
                  'total_connections_received': 1,
                  'pubsub_patterns': 0,
                  'aof_enabled': 0,
                  'used_cpu_sys': '0.02',
                  'used_memory_human': '709.12K',
                  'used_cpu_sys_children': '0.00',
                  'blocked_clients': 0,
                  'used_cpu_user': '0.00',
                  'client_biggest_input_buf': 0,
                  'arch_bits': 64,
                  'mem_fragmentation_ratio': '9.99',
                  'expired_keys': 0,
                  'evicted_keys': 0,
                  'bgsave_in_progress': 0,
                  'client_longest_output_list': 0,
                  'mem_allocator': 'jemalloc-2.2.5',
                  'process_id': 3020,
                  'uptime_in_seconds': 32,
                  'changes_since_last_save': 0,
                  'redis_git_dirty': 0,
                  'keyspace_hits': 0
                  }
        data_2 = {'pubsub_channels': 1,
                  'used_memory_peak_human': '1700.71K',
                  'bgrewriteaof_in_progress': 4,
                  'connected_slaves': 2,
                  'uptime_in_days': 1,
                  'multiplexing_api': 'epoll',
                  'lru_clock': 5954113,
                  'last_save_time': 51351718385,
                  'redis_version': '2.4.10',
                  'redis_git_sha1': 0,
                  'gcc_version': '4.4.6',
                  'connected_clients': 100,
                  'keyspace_misses': 670,
                  'used_memory': 1726144,
                  'vm_enabled': 0,
                  'used_cpu_user_children': '2.00',
                  'used_memory_peak': 1717528,
                  'role': 'master',
                  'total_commands_processed': 19764,
                  'latest_fork_usec': 8,
                  'loading': 0,
                  'used_memory_rss': 17254016,
                  'total_connections_received': 18764,
                  'pubsub_patterns': 0,
                  'aof_enabled': 0,
                  'used_cpu_sys': '0.05',
                  'used_memory_human': '1709.12K',
                  'used_cpu_sys_children': '0.09',
                  'blocked_clients': 8,
                  'used_cpu_user': '0.09',
                  'client_biggest_input_buf': 40,
                  'arch_bits': 64,
                  'mem_fragmentation_ratio': '0.99',
                  'expired_keys': 0,
                  'evicted_keys': 0,
                  'bgsave_in_progress': 0,
                  'client_longest_output_list': 0,
                  'mem_allocator': 'jemalloc-2.2.5',
                  'process_id': 3020,
                  'uptime_in_seconds': 95732,
                  'changes_since_last_save': 759,
                  'redis_git_dirty': 0,
                  'keyspace_hits': 5700
                  }

        with patch.object(RedisCollector, '_get_info',
                          Mock(return_value=data_1)):
            with patch('time.time', Mock(return_value=10)):
                self.collector.collect()

        self.assertPublishedMany(publish_mock, {})

        with patch.object(RedisCollector, '_get_info',
                          Mock(return_value=data_2)):
            with patch('time.time', Mock(return_value=20)):
                self.collector.collect()

        metrics = {'6379.process.uptime': 95732,
                   '6379.pubsub.channels': 1,
                   '6379.slaves.connected': 2,
                   '6379.process.connections_received': 18764,
                   '6379.clients.longest_output_list': 0,
                   '6379.process.commands_processed': 19764,
                   '6379.last_save.changes_since': 759,
                   '6379.memory.external_view': 17254016,
                   '6379.memory.fragmentation_ratio': 0.99,
                   '6379.last_save.time': 51351718385,
                   '6379.clients.connected': 100,
                   '6379.clients.blocked': 8,
                   '6379.pubsub.patterns': 0,
                   '6379.cpu.parent.user': 0.09,
                   '6379.last_save.time_since': -51351718365,
                   '6379.memory.internal_view': 1726144,
                   '6379.cpu.parent.sys': 0.05,
                   '6379.keyspace.misses': 670,
                   '6379.keys.expired': 0,
                   '6379.keys.evicted': 0,
                   '6379.keyspace.hits': 5700,
                   }

        self.assertPublishedMany(publish_mock, metrics)

        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])

################################################################################
if __name__ == "__main__":
    unittest.main()
