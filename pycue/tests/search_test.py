#!/usr/bin/env python

#  Copyright (c) 2018 Sony Pictures Imageworks Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
import mock
import unittest

import opencue
from opencue.compiled_proto import job_pb2
from opencue.compiled_proto import host_pb2


@mock.patch('opencue.cuebot.Cuebot.getStub')
class JobSearchTests(unittest.TestCase):

    def testByOptions(self, getStubMock):
        jobId = 'A0000000-0000-0000-0000-000000000000'
        stubMock = mock.Mock()
        getStubMock.return_value = stubMock

        opencue.search.JobSearch.byOptions(show=['pipe'], match=['v6'])

        stubMock.GetJobs.assert_called_with(
            job_pb2.JobGetJobsRequest(r=job_pb2.JobSearchCriteria(shows=['pipe'], substr=['v6'])),
            timeout=mock.ANY)

        opencue.search.JobSearch.byOptions(id=[jobId])

        stubMock.GetJobs.assert_called_with(
            job_pb2.JobGetJobsRequest(r=job_pb2.JobSearchCriteria(ids=[jobId])),
            timeout=mock.ANY)

    def testBaseSearchHost(self, getStubMock):
        stubMock = mock.Mock()
        stubMock.GetHosts.return_value = host_pb2.HostGetHostsResponse()
        getStubMock.return_value = stubMock

        hostSearch = opencue.search.HostSearch(substr=['unittest_host'])
        hostSearch.search()

        stubMock.GetHosts.assert_called_with(
            host_pb2.HostGetHostsRequest(r=host_pb2.HostSearchCriteria(substr=['unittest_host'])),
            timeout=mock.ANY)

    def testBaseSearchJob(self, getStubMock):
        stubMock = mock.Mock()
        getStubMock.return_value = stubMock

        jobSearch = opencue.search.JobSearch(show=['pipe'], match=['v6'])
        jobSearch.search()

        stubMock.GetJobs.assert_called_with(
            job_pb2.JobGetJobsRequest(r=job_pb2.JobSearchCriteria(shows=['pipe'], substr=['v6'])),
            timeout=mock.ANY)


if __name__ == '__main__':
    unittest.main()
