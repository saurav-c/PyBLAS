#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> vector;

BOOST_PYTHON_MODULE(utils)
{
    class_<vector>("Vector")
    	.def(init<unsigned int>())
    	.def(init<vector>())
    	.def("size", &vector::size)
    	.def("resize", &vector::resize)
    	.def("max_size", &vector::max_size)
    	.def("empty", &vector::empty)
    ;
}

