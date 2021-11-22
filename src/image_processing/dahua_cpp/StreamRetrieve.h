#include "Infra/Thread.h"
#include "GenICam/StreamSource.h"

using namespace Dahua::GenICam;
using namespace Dahua::Infra;

extern int shmid_point_id_input;
class StreamRetrieve : public CThread
{
public:
	StreamRetrieve(IStreamSourcePtr& streamSptr);
	bool start();
	bool stop();

private:
	void threadProc();
	bool m_isLoop;
	IStreamSourcePtr m_streamSptr;
};
