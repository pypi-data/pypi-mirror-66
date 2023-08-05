#ifndef __TRACYTHREAD_HPP__
#define __TRACYTHREAD_HPP__

#if defined _WIN32 || defined __CYGWIN__
#  include <windows.h>
#else
#  include <pthread.h>
#endif

namespace tracy
{

#if defined _WIN32 || defined __CYGWIN__

class Thread
{
public:
    Thread( void(*func)( void* ptr ), void* ptr )
        : m_func( func )
        , m_ptr( ptr )
        , m_hnd( CreateThread( nullptr, 0, Launch, this, 0, nullptr ) )
    {}

    ~Thread()
    {
        WaitForSingleObject( m_hnd, INFINITE );
        CloseHandle( m_hnd );
    }

    HANDLE Handle() const { return m_hnd; }

private:
    static DWORD WINAPI Launch( void* ptr ) { ((Thread*)ptr)->m_func( ((Thread*)ptr)->m_ptr ); return 0; }

    void(*m_func)( void* ptr );
    void* m_ptr;
    HANDLE m_hnd;
};

#else

class Thread
{
public:
    Thread( void(*func)( void* ptr ), void* ptr )
        : m_func( func )
        , m_ptr( ptr )
    {
        pthread_create( &m_thread, nullptr, Launch, this );
    }

    ~Thread()
    {
        pthread_join( m_thread, nullptr );
    }

    pthread_t Handle() const { return m_thread; }

private:
    static void* Launch( void* ptr ) { ((Thread*)ptr)->m_func( ((Thread*)ptr)->m_ptr ); return nullptr; }
    void(*m_func)( void* ptr );
    void* m_ptr;
    pthread_t m_thread;
};

#endif

}

#endif
