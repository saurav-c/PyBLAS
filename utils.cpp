#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

#include <vector>
using namespace boost::python;

typedef boost::numeric::ublas::vector<double> Vector;

BOOST_PYTHON_MODULE(utils)
{
    class_<Vector>("Vector")
    	.def(init<unsigned int>())
    	.def(init<Vector>())
    	.def("size", &Vector::size)
    	.def("resize", &Vector::resize)
    	.def("max_size", &Vector::max_size)
    	.def("empty", &Vector::empty)
    	.def(vector_indexing_suite<std::vector<Vector>>())
    ;
}

