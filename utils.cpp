#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> Vector;

double get(Vector vector, unsigned int index) {
	return vector(index)
}

BOOST_PYTHON_MODULE(utils)
{
    class_<Vector>("Vector")
    	.def(init<unsigned int>())
    	.def(init<Vector>())
    	.def("size", &Vector::size)
    	.def("resize", &Vector::resize)
    	.def("max_size", &Vector::max_size)
    	.def("empty", &Vector::empty)
    	.def("__getitem__", &Vector::operator, arg("index"),
    	return_internal_reference<>())
    	
    ;
}

