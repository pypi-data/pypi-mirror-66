#include "Adj.h"
#include "AdjustImpl.h"

Adj* Adj::instance = nullptr;

Adj::Adj()
	: m_adjustImpl(new AdjustImpl())
{
	LOG("Adjust()");
}
Adj::~Adj()
{
	LOG("~Adjust()");
}

void Adj::init(uint32_t secretId, uint32_t info1, uint32_t info2, uint32_t info3, uint32_t info4, bool debug)
{
	m_adjustImpl->Init(secretId, info1, info2, info3, info4, debug);
}

void Adj::release()
{
	m_adjustImpl->Release();
}

void Adj::logEvent(const char* eventType, std::map<std::string, std::string> eventValue)
{
	m_adjustImpl->logEvent(eventType, eventValue);
}
