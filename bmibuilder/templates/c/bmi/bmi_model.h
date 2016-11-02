#ifndef BMI_{{ name|upper }}_H_INCLUDED
#define BMI_{{ name|upper }}_H_INCLUDED

#if defined(__cplusplus)
extern "C" {
#endif

#include "bmi.h"

BMI_Model *register_bmi_{{ name }}(BMI_Model *model);

#if defined(__cplusplus)
}
#endif

#endif
