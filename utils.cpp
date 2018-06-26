#include <boost/python.hpp>
#include <boost/numeric/ublas/vector.hpp>

using namespace boost::python;

typedef boost::numeric::ublas::vector<double> BaseVector;

class Vector : public BaseVector {
public:
	void set(unsigned int index, double value) {
		(*this)(index) = value;
	}

	double get(unsigned int index) {
		return (*this)(index);
	}
}; 

BOOST_PYTHON_MODULE(utils)
{
    class_<Vector>("Vector")
    	.def(init<unsigned int>())
    	.def(init<Vector>())
    	.def("size", &Vector::size)
    	.def("resize", &Vector::resize)
    	.def("max_size", &Vector::max_size)
    	.def("empty", &Vector::empty)
    	.def("set", &Vector::set)
    	.def("get", &Vector::get)
    ;
}

