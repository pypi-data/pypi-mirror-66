// MIT License
//
// Copyright (c) 2020, The Regents of the University of California,
// through Lawrence Berkeley National Laboratory (subject to receipt of any
// required approvals from the U.S. Dept. of Energy).  All rights reserved.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#pragma once

#include "timemory/timemory.hpp"

// C++ includes
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <thread>
#include <type_traits>
#include <vector>

// C includes
#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>

#if defined(TIMEMORY_USE_LIBEXPLAIN)
#    include <libexplain/execvp.h>
#endif

#if defined(_UNIX)
#    include <unistd.h>
extern "C"
{
    extern char** environ;
}
#endif

namespace tim
{
namespace sampling
{
//
//--------------------------------------------------------------------------------------//
//
template <typename CompT, size_t N>
struct sampler;
//
//--------------------------------------------------------------------------------------//
//
template <template <typename...> class CompT, size_t N, typename... Types>
struct sampler<CompT<Types...>, N>
{
    using this_type    = sampler<CompT<Types...>, N>;
    using components_t = CompT<Types...>;
    using array_t      = std::array<components_t, N>;
    using signal_set_t = std::set<int>;

    static void  execute(int signum);
    static void  execute(int signum, siginfo_t*, void*);
    static auto& get_samplers() { return get_persistent_data().m_instances; }

    sampler(const std::string& _label, signal_set_t _good,
            signal_set_t _bad = signal_set_t{})
    : m_idx(0)
    , m_good(_good)
    , m_bad(_bad)
    {
        m_data.fill(components_t(_label));
    }

    void sample()
    {
        auto& c = m_data.at((m_idx++) % N);
        c.sample();
    }

    void start()
    {
        for(auto& itr : m_data)
            itr.start();
    }

    void stop()
    {
        for(auto& itr : m_data)
            itr.stop();
    }

    bool is_good(int v) const { return m_good.count(v) > 0; }
    bool is_bad(int v) const { return m_bad.count(v) > 0; }

protected:
    size_t       m_idx  = 0;
    signal_set_t m_good = {};
    signal_set_t m_bad  = {};
    array_t      m_data = {};

private:
    struct persistent_data
    {
        struct sigaction        m_sigaction;
        struct itimerval        m_itimerval;
        std::vector<this_type*> m_instances;
    };

    static persistent_data& get_persistent_data()
    {
        static persistent_data _instance;
        return _instance;
    }
};
//
//--------------------------------------------------------------------------------------//
//
template <template <typename...> class CompT, size_t N, typename... Types>
void
sampler<CompT<Types...>, N>::execute(int signum)
{
    for(auto& itr : get_samplers())
    {
        if(itr->is_good(signum))
        {
            itr->sample();
        }
        else if(itr->is_bad(signum))
        {
            perror("timem sampler caught signal that was not TIMEM_SIGNAL...");
            signal(signum, SIG_DFL);
            raise(signum);
        }
    }
}
//
//--------------------------------------------------------------------------------------//
//
template <template <typename...> class CompT, size_t N, typename... Types>
void
sampler<CompT<Types...>, N>::execute(int signum, siginfo_t*, void*)
{
    for(auto& itr : get_samplers())
    {
        if(itr->is_good(signum))
        {
            itr->sample();
        }
        else if(itr->is_bad(signum))
        {
            perror("timem sampler caught signal that was not TIMEM_SIGNAL...");
            signal(signum, SIG_DFL);
            raise(signum);
        }
    }
}
//
//--------------------------------------------------------------------------------------//
//
}  // namespace sampling
}  // namespace tim
