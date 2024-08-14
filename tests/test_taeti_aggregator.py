import unittest

from taetitool.model.issue import Issue
from taetitool.taeti_aggregator import TaetiAggregator
from taetitool.util import DefaultKeyDict


class TestTaetiAggretator(unittest.TestCase):
    def test_valid_file(self):
        taeti_file_path = 'files/20240215-valid.taeti'

        default_issue = Issue(None, None, 'Default project', 'Default task')

        issue_data = DefaultKeyDict(default_issue, {
            '1123': Issue(1123, 'Data import for CSV', 'ACME', 'Customizing',
                          'Data import'),
            '1987': Issue(1987, 'None', 'ACME', 'Customizing', 'Testing'),
            '3123': Issue(3123, 'Support case 221', 'PI Fan AG',
                          'Remote Support', ''),
            '3987': Issue(3987, 'Configuration of another feature for tenant X',
                          'PI Fan AG', 'Configuration', ''),
            '5123': Issue(5123, 'None', 'Fancy Project',
                          'AP02-01 Concept Module A', ''),
            '5124': Issue(5124, 'None', 'Fancy Project',
                          'AP02-01 Concept Module B', ''),
            '5223': Issue(5223, 'Implementation of Module A', 'Fancy Project',
                          'AP02-02 Implementation Module A', ''),
            '5224': Issue(5224, 'Implementation of Module B', 'Fancy Project',
                          'AP02-02 Implementation Module B', ''),
            '7123': Issue(7123, 'Support case 223', 'Support', '', ''),
            '7987': Issue(7987, 'Support case 227', 'Support', '', ''),
            '7124': Issue(7124, 'Support case 224', 'Default project',
                          'Default task', 'None')
        })

        assignment_rules = [
            {
                'name': 'break',
                'attribute': 'description',
                'pattern': 'Break|^Private',
                'project': 'Break',
                'task': 'Break'
            },
            {
                'name': 'meeting',
                'attribute': 'description',
                'pattern': 'Daily|Weekly|Sprint Retrospective|Product Management Round Table',
                'project': 'Internal tasks',
                'task': 'Meeting'
            },
            {
                'name': 'support',
                'attribute': 'project',
                'pattern': 'Support',
                'project': 'External tasks',
                'task': 'Support'
            }
        ]

        expected_taetis = {
            "Default project": {
                "time": 4800,
                "Default task": {
                    "time": 4800,
                    "None": {
                        "time": 4800,
                        "9987": {
                            "time": 3000
                        },
                        "9123": {
                            "time": 1800
                        }
                    }
                }
            },
            "ACME": {
                "time": 4800,
                "Customizing": {
                    "time": 4800,
                    "Data import": {
                        "time": 2100,
                        "1123": {
                            "time": 2100
                        }
                    },
                    "Testing": {
                        "time": 2700,
                        "1987": {
                            "time": 2700
                        }
                    }
                }
            },
            "None": {
                "time": 8100,
                "None": {
                    "time": 8100,
                    "None": {
                        "time": 8100,
                        "None": {
                            "time": 8100
                        }
                    }
                }
            },
            "Break": {
                "time": 4500,
                "Break": {
                    "time": 4500,
                    "None": {
                        "time": 4500,
                        "None": {
                            "time": 4500
                        }
                    }
                }
            },
            "Internal tasks": {
                "time": 3000,
                "Meeting": {
                    "time": 3000,
                    "None": {
                        "time": 3000,
                        "None": {
                            "time": 3000
                        }
                    }
                }
            },
            "PI Fan AG": {
                "time": 600,
                "Remote Support": {
                    "time": 300,
                    "None": {
                        "time": 300,
                        "3123": {
                            "time": 300
                        }
                    }
                },
                "Configuration": {
                    "time": 300,
                    "None": {
                        "time": 300,
                        "3987": {
                            "time": 300
                        }
                    }
                }
            },
            "Fancy Project": {
                "time": 4200,
                "AP02-01 Concept Module A": {
                    "time": 1500,
                    "None": {
                        "time": 1500,
                        "5123": {
                            "time": 1500
                        }
                    }
                },
                "AP02-01 Concept Module B": {
                    "time": 1200,
                    "None": {
                        "time": 1200,
                        "5124": {
                            "time": 1200
                        }
                    }
                },
                "AP02-02 Implementation Module A": {
                    "time": 900,
                    "None": {
                        "time": 900,
                        "5223": {
                            "time": 900
                        }
                    }
                },
                "AP02-02 Implementation Module B": {
                    "time": 600,
                    "None": {
                        "time": 600,
                        "5224": {
                            "time": 600
                        }
                    }
                }
            },
            "External tasks": {
                "time": 2700,
                "Support": {
                    "time": 2700,
                    "None": {
                        "time": 2700,
                        "7123": {
                            "time": 1800
                        },
                        "7987": {
                            "time": 900
                        }
                    }
                }
            }
        }

        taeti_aggregator = TaetiAggregator(issue_data, assignment_rules)
        taeti_aggretation = taeti_aggregator.process(taeti_file_path)

        taeti_aggretaion_json = taeti_aggretation.to_json()

        self.maxDiff = None

        self.assertEqual(taeti_aggretaion_json['date'], 'Thursday, 15.02.2024')
        self.assertEqual(taeti_aggretaion_json['day_total_time'], 34200)
        self.assertDictEqual(taeti_aggretaion_json['taetis'], expected_taetis)

    def test_valid_file_single_space_format(self):
        taeti_file_path = 'files/20240216-valid.taeti'

        default_issue = Issue(None, None, 'Default project', 'Default task')

        issue_data = DefaultKeyDict(default_issue, {
            '1123': Issue(1123, 'Data import for CSV', 'ACME', 'Customizing',
                          'Data import'),
            '1987': Issue(1987, 'None', 'ACME', 'Customizing', 'Testing'),
            '3123': Issue(3123, 'Support case 221', 'PI Fan AG',
                          'Remote Support', ''),
            '3987': Issue(3987, 'Configuration of another feature for tenant X',
                          'PI Fan AG', 'Configuration', ''),
            '5123': Issue(5123, 'None', 'Fancy Project',
                          'AP02-01 Concept Module A', ''),
            '5124': Issue(5124, 'None', 'Fancy Project',
                          'AP02-01 Concept Module B', ''),
            '5223': Issue(5223, 'Implementation of Module A', 'Fancy Project',
                          'AP02-02 Implementation Module A', ''),
            '5224': Issue(5224, 'Implementation of Module B', 'Fancy Project',
                          'AP02-02 Implementation Module B', ''),
            '7123': Issue(7123, 'Support case 223', 'Support', '', ''),
            '7987': Issue(7987, 'Support case 227', 'Support', '', ''),
            '7124': Issue(7124, 'Support case 224', 'Default project',
                          'Default task', 'None')
        })

        assignment_rules = [
            {
                'name': 'break',
                'attribute': 'description',
                'pattern': 'Break|^Private',
                'project': 'Break',
                'task': 'Break'
            },
            {
                'name': 'meeting',
                'attribute': 'description',
                'pattern': 'Daily|Weekly|Sprint Retrospective|Product Management Round Table',
                'project': 'Internal tasks',
                'task': 'Meeting'
            },
            {
                'name': 'support',
                'attribute': 'project',
                'pattern': 'Support',
                'project': 'External tasks',
                'task': 'Support'
            }
        ]

        expected_taetis = {
            "Default project": {
                "time": 4800,
                "Default task": {
                    "time": 4800,
                    "None": {
                        "time": 4800,
                        "9987": {
                            "time": 3000
                        },
                        "9123": {
                            "time": 1800
                        }
                    }
                }
            },
            "ACME": {
                "time": 4800,
                "Customizing": {
                    "time": 4800,
                    "Data import": {
                        "time": 2100,
                        "1123": {
                            "time": 2100
                        }
                    },
                    "Testing": {
                        "time": 2700,
                        "1987": {
                            "time": 2700
                        }
                    }
                }
            },
            "None": {
                "time": 8100,
                "None": {
                    "time": 8100,
                    "None": {
                        "time": 8100,
                        "None": {
                            "time": 8100
                        }
                    }
                }
            },
            "Break": {
                "time": 4500,
                "Break": {
                    "time": 4500,
                    "None": {
                        "time": 4500,
                        "None": {
                            "time": 4500
                        }
                    }
                }
            },
            "Internal tasks": {
                "time": 3000,
                "Meeting": {
                    "time": 3000,
                    "None": {
                        "time": 3000,
                        "None": {
                            "time": 3000
                        }
                    }
                }
            },
            "PI Fan AG": {
                "time": 600,
                "Remote Support": {
                    "time": 300,
                    "None": {
                        "time": 300,
                        "3123": {
                            "time": 300
                        }
                    }
                },
                "Configuration": {
                    "time": 300,
                    "None": {
                        "time": 300,
                        "3987": {
                            "time": 300
                        }
                    }
                }
            },
            "Fancy Project": {
                "time": 4200,
                "AP02-01 Concept Module A": {
                    "time": 1500,
                    "None": {
                        "time": 1500,
                        "5123": {
                            "time": 1500
                        }
                    }
                },
                "AP02-01 Concept Module B": {
                    "time": 1200,
                    "None": {
                        "time": 1200,
                        "5124": {
                            "time": 1200
                        }
                    }
                },
                "AP02-02 Implementation Module A": {
                    "time": 900,
                    "None": {
                        "time": 900,
                        "5223": {
                            "time": 900
                        }
                    }
                },
                "AP02-02 Implementation Module B": {
                    "time": 600,
                    "None": {
                        "time": 600,
                        "5224": {
                            "time": 600
                        }
                    }
                }
            },
            "External tasks": {
                "time": 2700,
                "Support": {
                    "time": 2700,
                    "None": {
                        "time": 2700,
                        "7123": {
                            "time": 1800
                        },
                        "7987": {
                            "time": 900
                        }
                    }
                }
            }
        }

        taeti_aggregator = TaetiAggregator(issue_data, assignment_rules)
        taeti_aggretation = taeti_aggregator.process(taeti_file_path)

        taeti_aggretaion_json = taeti_aggretation.to_json()

        self.maxDiff = None

        self.assertEqual(taeti_aggretaion_json['date'], 'Friday, 16.02.2024')
        self.assertEqual(taeti_aggretaion_json['day_total_time'], 34200)
        self.assertDictEqual(taeti_aggretaion_json['taetis'], expected_taetis)

if __name__ == '__main__':
    unittest.main()
