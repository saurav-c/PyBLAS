#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

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
    	.def("swap", &Vector::swap)
    	.def("insert_element", &Vector::insert_element)
    	.def("erase_element", &Vector::erase_element)
    	.def("clear", &Vector::clear)
    	// .def("begin", &Vector::begin)
    	// .def("end", &Vector::end)
    	// .def("rbegin", &Vector::rbegin)
    	// .def("rend", &Vector::rend)
    	.def(vector_indexing_suite<std::vector<double>>())
    ;
}

