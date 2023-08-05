#ifndef __TRACYSOCKET_HPP__
#define __TRACYSOCKET_HPP__

#include <functional>

struct sockaddr;

namespace tracy
{

#ifdef _WIN32
void InitWinSock();
#endif

class Socket
{
    enum { BufSize = 128 * 1024 };

public:
    Socket();
    Socket( int sock );
    ~Socket();

    bool Connect( const char* addr, int port );
    void Close();

    int Send( const void* buf, int len );
    int GetSendBufSize();

    bool Read( void* buf, int len, int timeout, std::function<bool()> exitCb );
    bool ReadRaw( void* buf, int len, int timeout );
    bool HasData();

    Socket( const Socket& ) = delete;
    Socket( Socket&& ) = delete;
    Socket& operator=( const Socket& ) = delete;
    Socket& operator=( Socket&& ) = delete;

private:
    int RecvBuffered( void* buf, int len, int timeout );
    int Recv( void* buf, int len, int timeout );

    char* m_buf;
    char* m_bufPtr;
    int m_sock;
    int m_bufLeft;
};

class ListenSocket
{
public:
    ListenSocket();
    ~ListenSocket();

    bool Listen( int port, int backlog );
    Socket* Accept();
    void Close();

    ListenSocket( const ListenSocket& ) = delete;
    ListenSocket( ListenSocket&& ) = delete;
    ListenSocket& operator=( const ListenSocket& ) = delete;
    ListenSocket& operator=( ListenSocket&& ) = delete;

private:
    int m_sock;
};

class UdpBroadcast
{
public:
    UdpBroadcast();
    ~UdpBroadcast();

    bool Open( const char* addr, int port );
    void Close();

    int Send( int port, const void* data, int len );

    UdpBroadcast( const UdpBroadcast& ) = delete;
    UdpBroadcast( UdpBroadcast&& ) = delete;
    UdpBroadcast& operator=( const UdpBroadcast& ) = delete;
    UdpBroadcast& operator=( UdpBroadcast&& ) = delete;

private:
    int m_sock;
};

class IpAddress
{
public:
    IpAddress();
    ~IpAddress();

    void Set( const struct sockaddr& addr );

    uint32_t GetNumber() const { return m_number; }
    const char* GetText() const { return m_text; }

    IpAddress( const IpAddress& ) = delete;
    IpAddress( IpAddress&& ) = delete;
    IpAddress& operator=( const IpAddress& ) = delete;
    IpAddress& operator=( IpAddress&& ) = delete;

private:
    uint32_t m_number;
    char m_text[17];
};

class UdpListen
{
public:
    UdpListen();
    ~UdpListen();

    bool Listen( int port );
    void Close();

    const char* Read( size_t& len, IpAddress& addr );

    UdpListen( const UdpListen& ) = delete;
    UdpListen( UdpListen&& ) = delete;
    UdpListen& operator=( const UdpListen& ) = delete;
    UdpListen& operator=( UdpListen&& ) = delete;

private:
    int m_sock;
};

}

#endif
