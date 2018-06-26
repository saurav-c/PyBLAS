#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> vector;

BOOST_PYTHON_MODULE(utils)
{
    class_<vector>("Vector")
    	.def(init<unsigned int>())
    ;
}

