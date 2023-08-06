/*****************************************************************************
   Copyright 2004-2008 Steve MÃƒÂ©nard

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

	   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

 *****************************************************************************/
#include <Python.h>
#include "jpype.h"

/*****************************************************************************/
// Local frames represent the JNIEnv for memory handling all java
// resources should be created within them.
//

JPJavaFrame::JPJavaFrame(JPContext* context, JNIEnv* p_env, int i)
: m_Context(context), m_Env(p_env), popped(false)
{
	// Create a memory management frame to live in
	m_Env->functions->PushLocalFrame(m_Env, i);
}

JPJavaFrame::JPJavaFrame(JPContext* context, int i)
: m_Context(context), popped(false)
{
	m_Env = context->getEnv();

	// Create a memory management frame to live in
	m_Env->functions->PushLocalFrame(m_Env, i);
}

JPJavaFrame::JPJavaFrame(const JPJavaFrame& frame)
: m_Context(frame.m_Context), m_Env(frame.m_Env), popped(false)
{
	// Create a memory management frame to live in
	m_Env->functions->PushLocalFrame(m_Env, LOCAL_FRAME_DEFAULT);
}

jobject JPJavaFrame::keep(jobject obj)
{
	popped = true;
	return m_Env->functions->PopLocalFrame(m_Env, obj);
}

JPJavaFrame::~JPJavaFrame()
{
	// Check if we have already closed the frame.
	if (!popped)
	{
		m_Env->functions->PopLocalFrame(m_Env, NULL);
	}

	// It is not safe to detach as we would loss all local references including
	// any we want to keep.
}

void JPJavaFrame::DeleteLocalRef(jobject obj)
{
	m_Env->DeleteLocalRef(obj);
}

void JPJavaFrame::DeleteGlobalRef(jobject obj)
{
	m_Env->DeleteGlobalRef(obj);
}

jweak JPJavaFrame::NewWeakGlobalRef(jobject obj)
{
	return m_Env->NewWeakGlobalRef(obj);
}

void JPJavaFrame::DeleteWeakGlobalRef(jweak obj)
{
	return m_Env->DeleteWeakGlobalRef(obj);
}

jobject JPJavaFrame::NewLocalRef(jobject a0)
{
	jobject res = m_Env->functions->NewLocalRef(m_Env, a0);
	return res;
}

jobject JPJavaFrame::NewGlobalRef(jobject a0)
{
	JP_TRACE_IN("JPJavaFrame::NewGlobalRef", a0);
	jobject res = m_Env->functions->NewGlobalRef(m_Env, a0);
	JP_TRACE("got", res);
	return res;
	JP_TRACE_OUT;
}

/*****************************************************************************/
// Exceptions

bool JPJavaFrame::ExceptionCheck()
{
	return (m_Env->functions->ExceptionCheck(m_Env) ? true : false);
}

void JPJavaFrame::ExceptionDescribe()
{
	m_Env->functions->ExceptionDescribe(m_Env);
}

void JPJavaFrame::ExceptionClear()
{
	m_Env->functions->ExceptionClear(m_Env);
}

jint JPJavaFrame::ThrowNew(jclass clazz, const char* msg)
{
	return m_Env->functions->ThrowNew(m_Env, clazz, msg);
}

jint JPJavaFrame::Throw(jthrowable th)
{
	return m_Env->functions->Throw(m_Env, th);
}

jthrowable JPJavaFrame::ExceptionOccurred()
{
	jthrowable res;

	res = m_Env->functions->ExceptionOccurred(m_Env);
#ifdef JP_TRACING_ENABLE
	if (res)
	{
		m_Env->functions->ExceptionDescribe(m_Env);
	}
#endif
	return res;
}

/*****************************************************************************/

#ifdef JP_INSTRUMENTATION
#define JAVA_RETURN(X,Y,Z) \
  PyJPModuleFault_throw(compile_hash(Y)); \
  X ret = Z; \
  check(); \
  return ret;
#define JAVA_CHECK(Y,Z) \
  PyJPModuleFault_throw(compile_hash(Y)); \
  Z; \
  check();
#else
#define JAVA_RETURN(X,Y,Z) \
  X ret = Z; \
  check(); \
  return ret;
#define JAVA_CHECK(Y,Z) \
  Z; \
  check();
#endif

void JPJavaFrame::check()
{
	if (m_Env && m_Env->functions->ExceptionCheck(m_Env) == JNI_TRUE)
	{
		jthrowable th = m_Env->functions->ExceptionOccurred(m_Env);
		m_Env->functions->ExceptionClear(m_Env);
		throw JPypeException(*this, th, JP_STACKINFO());
	}
}

jobject JPJavaFrame::NewObjectA(jclass a0, jmethodID a1, jvalue* a2)
{
	jobject res;
	// Allocate the object
	JAVA_CHECK("JPJavaFrame::JPJavaFrame::NewObjectA",
			res = m_Env->functions->AllocObject(m_Env, a0));
	JAVA_CHECK("JPJavaFrame::NewObjectA::AllocObject",
			m_Env->functions->CallVoidMethodA(m_Env, res, a1, a2));

	// Initialize the object
	return res;
}

jobject JPJavaFrame::NewDirectByteBuffer(void* address, jlong capacity)
{
	JAVA_RETURN(jobject, "JPJavaFrame::NewDirectByteBuffer",
		m_Env->functions->NewDirectByteBuffer(m_Env, address, capacity));
}

/*****************************************************************************/

jbyte JPJavaFrame::GetStaticByteField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jbyte, "JPJavaFrame::GetStaticByteField",
		m_Env->functions->GetStaticByteField(m_Env, clazz, fid));
}

jbyte JPJavaFrame::GetByteField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jbyte, "JPJavaFrame::GetByteField",
		m_Env->functions->GetByteField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticByteField(jclass clazz, jfieldID fid, jbyte val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticByteField",
		m_Env->functions->SetStaticByteField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetByteField(jobject clazz, jfieldID fid, jbyte val)
{
	JAVA_CHECK("JPJavaFrame::SetByteField",
		m_Env->functions->SetByteField(m_Env, clazz, fid, val));
}

jbyte JPJavaFrame::CallStaticByteMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jbyte, "JPJavaFrame::CallStaticByteMethodA",
		m_Env->functions->CallStaticByteMethodA(m_Env, clazz, mid, val));
}

jbyte JPJavaFrame::CallByteMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jbyte, "JPJavaFrame::CallByteMethodA",
		m_Env->functions->CallByteMethodA(m_Env, obj, mid, val));
}

jbyte JPJavaFrame::CallNonvirtualByteMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jbyte, "JPJavaFrame::CallNonvirtualByteMethodA",
		m_Env->functions->CallNonvirtualByteMethodA(m_Env, obj, claz, mid, val));
}

jshort JPJavaFrame::GetStaticShortField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jshort, "JPJavaFrame::GetStaticShortField",
		m_Env->functions->GetStaticShortField(m_Env, clazz, fid));
}

jshort JPJavaFrame::GetShortField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jshort, "JPJavaFrame::GetShortField",
		m_Env->functions->GetShortField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticShortField(jclass clazz, jfieldID fid, jshort val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticShortField",
		m_Env->functions->SetStaticShortField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetShortField(jobject clazz, jfieldID fid, jshort val)
{
	JAVA_CHECK("JPJavaFrame::SetShortField",
		m_Env->functions->SetShortField(m_Env, clazz, fid, val));
}

jshort JPJavaFrame::CallStaticShortMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jshort, "JPJavaFrame::CallStaticShortMethodA",
		m_Env->functions->CallStaticShortMethodA(m_Env, clazz, mid, val));
}

jshort JPJavaFrame::CallShortMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jshort, "JPJavaFrame::CallShortMethodA",
		m_Env->functions->CallShortMethodA(m_Env, obj, mid, val));
}

jshort JPJavaFrame::CallNonvirtualShortMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jshort, "JPJavaFrame::CallNonvirtualShortMethodA",
		m_Env->functions->CallNonvirtualShortMethodA(m_Env, obj, claz, mid, val));
}

jint JPJavaFrame::GetStaticIntField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jint, "JPJavaFrame::GetStaticIntField",
		m_Env->functions->GetStaticIntField(m_Env, clazz, fid));
}

jint JPJavaFrame::GetIntField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jint, "JPJavaFrame::GetIntField",
		m_Env->functions->GetIntField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticIntField(jclass clazz, jfieldID fid, jint val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticIntField",
		m_Env->functions->SetStaticIntField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetIntField(jobject clazz, jfieldID fid, jint val)
{
	JAVA_CHECK("JPJavaFrame::SetIntField",
		m_Env->functions->SetIntField(m_Env, clazz, fid, val));
}

jint JPJavaFrame::CallStaticIntMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jint, "JPJavaFrame::CallStaticIntMethodA",
		m_Env->functions->CallStaticIntMethodA(m_Env, clazz, mid, val));
}

jint JPJavaFrame::CallIntMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jint, "JPJavaFrame::CallIntMethodA",
		m_Env->functions->CallIntMethodA(m_Env, obj, mid, val));
}

jint JPJavaFrame::CallNonvirtualIntMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jint, "JPJavaFrame::CallNonvirtualIntMethodA",
		m_Env->functions->CallNonvirtualIntMethodA(m_Env, obj, claz, mid, val));
}

jlong JPJavaFrame::GetStaticLongField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jlong, "JPJavaFrame::GetStaticLongField",
		m_Env->functions->GetStaticLongField(m_Env, clazz, fid));
}

jlong JPJavaFrame::GetLongField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jlong, "JPJavaFrame::GetLongField",
		m_Env->functions->GetLongField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticLongField(jclass clazz, jfieldID fid, jlong val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticLongField",
		m_Env->functions->SetStaticLongField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetLongField(jobject clazz, jfieldID fid, jlong val)
{
	JAVA_CHECK("JPJavaFrame::SetLongField",
		m_Env->functions->SetLongField(m_Env, clazz, fid, val));
}

jlong JPJavaFrame::CallStaticLongMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jlong, "JPJavaFrame::CallStaticLongMethodA",
		m_Env->functions->CallStaticLongMethodA(m_Env, clazz, mid, val));
}

jlong JPJavaFrame::CallLongMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jlong, "JPJavaFrame::CallLongMethodA",
		m_Env->functions->CallLongMethodA(m_Env, obj, mid, val));
}

jlong JPJavaFrame::CallNonvirtualLongMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jlong, "JPJavaFrame::CallNonvirtualLongMethodA",
		m_Env->functions->CallNonvirtualLongMethodA(m_Env, obj, claz, mid, val));
}

jfloat JPJavaFrame::GetStaticFloatField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jfloat, "JPJavaFrame::GetStaticFloatField",
		m_Env->functions->GetStaticFloatField(m_Env, clazz, fid));
}

jfloat JPJavaFrame::GetFloatField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jfloat, "JPJavaFrame::GetFloatField",
		m_Env->functions->GetFloatField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticFloatField(jclass clazz, jfieldID fid, jfloat val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticFloatField",
		m_Env->functions->SetStaticFloatField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetFloatField(jobject clazz, jfieldID fid, jfloat val)
{
	JAVA_CHECK("JPJavaFrame::SetFloatField",
		m_Env->functions->SetFloatField(m_Env, clazz, fid, val));
}

jfloat JPJavaFrame::CallStaticFloatMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jfloat, "JPJavaFrame::CallStaticFloatMethodA",
		m_Env->functions->CallStaticFloatMethodA(m_Env, clazz, mid, val));
}

jfloat JPJavaFrame::CallFloatMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jfloat, "JPJavaFrame::CallFloatMethodA",
		m_Env->functions->CallFloatMethodA(m_Env, obj, mid, val));
}

jfloat JPJavaFrame::CallNonvirtualFloatMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jfloat, "JPJavaFrame::CallNonvirtualFloatMethodA",
		m_Env->functions->CallNonvirtualFloatMethodA(m_Env, obj, claz, mid, val));
}

jdouble JPJavaFrame::GetStaticDoubleField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jdouble, "JPJavaFrame::GetStaticDoubleField",
		m_Env->functions->GetStaticDoubleField(m_Env, clazz, fid));
}

jdouble JPJavaFrame::GetDoubleField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jdouble, "JPJavaFrame::GetDoubleField",
		m_Env->functions->GetDoubleField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticDoubleField(jclass clazz, jfieldID fid, jdouble val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticDoubleField",
		m_Env->functions->SetStaticDoubleField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetDoubleField(jobject clazz, jfieldID fid, jdouble val)
{
	JAVA_CHECK("JPJavaFrame::SetDoubleField",
		m_Env->functions->SetDoubleField(m_Env, clazz, fid, val));
}

jdouble JPJavaFrame::CallStaticDoubleMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jdouble, "JPJavaFrame::CallStaticDoubleMethodA",
		m_Env->functions->CallStaticDoubleMethodA(m_Env, clazz, mid, val));
}

jdouble JPJavaFrame::CallDoubleMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jdouble, "JPJavaFrame::CallDoubleMethodA",
		m_Env->functions->CallDoubleMethodA(m_Env, obj, mid, val));
}

jdouble JPJavaFrame::CallNonvirtualDoubleMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jdouble, "JPJavaFrame::CallNonvirtualDoubleMethodA",
		m_Env->functions->CallNonvirtualDoubleMethodA(m_Env, obj, claz, mid, val));
}

jchar JPJavaFrame::GetStaticCharField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jchar, "JPJavaFrame::GetStaticCharField",
		m_Env->functions->GetStaticCharField(m_Env, clazz, fid));
}

jchar JPJavaFrame::GetCharField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jchar, "JPJavaFrame::GetCharField",
		m_Env->functions->GetCharField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticCharField(jclass clazz, jfieldID fid, jchar val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticCharField",
		m_Env->functions->SetStaticCharField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetCharField(jobject clazz, jfieldID fid, jchar val)
{
	JAVA_CHECK("JPJavaFrame::SetCharField",
		m_Env->functions->SetCharField(m_Env, clazz, fid, val));
}

jchar JPJavaFrame::CallStaticCharMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jchar, "JPJavaFrame::CallStaticCharMethodA",
		m_Env->functions->CallStaticCharMethodA(m_Env, clazz, mid, val));
}

jchar JPJavaFrame::CallCharMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jchar, "JPJavaFrame::CallCharMethodA",
		m_Env->functions->CallCharMethodA(m_Env, obj, mid, val));
}

jchar JPJavaFrame::CallNonvirtualCharMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jchar, "JPJavaFrame::CallNonvirtualCharMethodA",
		m_Env->functions->CallNonvirtualCharMethodA(m_Env, obj, claz, mid, val));
}

jboolean JPJavaFrame::GetStaticBooleanField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::GetStaticBooleanField",
		m_Env->functions->GetStaticBooleanField(m_Env, clazz, fid));
}

jboolean JPJavaFrame::GetBooleanField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::GetBooleanField",
		m_Env->functions->GetBooleanField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticBooleanField(jclass clazz, jfieldID fid, jboolean val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticBooleanField",
		m_Env->functions->SetStaticBooleanField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetBooleanField(jobject clazz, jfieldID fid, jboolean val)
{
	JAVA_CHECK("JPJavaFrame::SetBooleanField",
		m_Env->functions->SetBooleanField(m_Env, clazz, fid, val));
}

jboolean JPJavaFrame::CallStaticBooleanMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::CallStaticBooleanMethodA",
		m_Env->functions->CallStaticBooleanMethodA(m_Env, clazz, mid, val));
}

jboolean JPJavaFrame::CallBooleanMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::CallBooleanMethodA",
		m_Env->functions->CallBooleanMethodA(m_Env, obj, mid, val));
}

jboolean JPJavaFrame::CallNonvirtualBooleanMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::CallNonvirtualBooleanMethodA",
		m_Env->functions->CallNonvirtualBooleanMethodA(m_Env, obj, claz, mid, val));
}

jobject JPJavaFrame::GetStaticObjectField(jclass clazz, jfieldID fid)
{
	JAVA_RETURN(jobject, "JPJavaFrame::GetStaticObjectField",
		m_Env->functions->GetStaticObjectField(m_Env, clazz, fid));
}

jobject JPJavaFrame::GetObjectField(jobject clazz, jfieldID fid)
{
	JAVA_RETURN(jobject, "JPJavaFrame::GetObjectField",
		m_Env->functions->GetObjectField(m_Env, clazz, fid));
}

void JPJavaFrame::SetStaticObjectField(jclass clazz, jfieldID fid, jobject val)
{
	JAVA_CHECK("JPJavaFrame::SetStaticObjectField",
		m_Env->functions->SetStaticObjectField(m_Env, clazz, fid, val));
}

void JPJavaFrame::SetObjectField(jobject clazz, jfieldID fid, jobject val)
{
	JAVA_CHECK("JPJavaFrame::SetObjectField",
		m_Env->functions->SetObjectField(m_Env, clazz, fid, val));
}

jobject JPJavaFrame::CallStaticObjectMethodA(jclass clazz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jobject, "JPJavaFrame::CallStaticObjectMethodA",
		m_Env->functions->CallStaticObjectMethodA(m_Env, clazz, mid, val));
}

jobject JPJavaFrame::CallObjectMethodA(jobject obj, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jobject, "JPJavaFrame::CallObjectMethodA",
		m_Env->functions->CallObjectMethodA(m_Env, obj, mid, val));
}

jobject JPJavaFrame::CallNonvirtualObjectMethodA(jobject obj, jclass claz, jmethodID mid, jvalue* val)
{
	JAVA_RETURN(jobject, "JPJavaFrame::CallNonvirtualObjectMethodA",
		m_Env->functions->CallNonvirtualObjectMethodA(m_Env, obj, claz, mid, val));
}

jbyteArray JPJavaFrame::NewByteArray(jsize len)
{
	JAVA_RETURN(jbyteArray, "JPJavaFrame::NewByteArray",
		m_Env->functions->NewByteArray(m_Env, len));
}

void JPJavaFrame::SetByteArrayRegion(jbyteArray array, jsize start, jsize len, jbyte* vals)
{
	JAVA_CHECK("JPJavaFrame::SetByteArrayRegion",
		m_Env->functions->SetByteArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetByteArrayRegion(jbyteArray array, jsize start, jsize len, jbyte* vals)
{
	JAVA_CHECK("JPJavaFrame::GetByteArrayRegion",
		m_Env->functions->GetByteArrayRegion(m_Env, array, start, len, vals));
}

jbyte* JPJavaFrame::GetByteArrayElements(jbyteArray array, jboolean* isCopy)
{
	JAVA_RETURN(jbyte*, "JPJavaFrame::GetByteArrayElements",
		m_Env->functions->GetByteArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseByteArrayElements(jbyteArray array, jbyte* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseByteArrayElements",
		m_Env->functions->ReleaseByteArrayElements(m_Env, array, v, mode));
}

jshortArray JPJavaFrame::NewShortArray(jsize len)
{
	JAVA_RETURN(jshortArray, "JPJavaFrame::NewShortArray",
		m_Env->functions->NewShortArray(m_Env, len));
}

void JPJavaFrame::SetShortArrayRegion(jshortArray array, jsize start, jsize len, jshort* vals)
{
	JAVA_CHECK("JPJavaFrame::SetShortArrayRegion",
		m_Env->functions->SetShortArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetShortArrayRegion(jshortArray array, jsize start, jsize len, jshort* vals)
{
	JAVA_CHECK("JPJavaFrame::GetShortArrayRegion",
		m_Env->functions->GetShortArrayRegion(m_Env, array, start, len, vals));
}

jshort* JPJavaFrame::GetShortArrayElements(jshortArray array, jboolean* isCopy)
{
	JAVA_RETURN(jshort*, "JPJavaFrame::GetShortArrayElements",
		m_Env->functions->GetShortArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseShortArrayElements(jshortArray array, jshort* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseShortArrayElements",
		m_Env->functions->ReleaseShortArrayElements(m_Env, array, v, mode));
}

jintArray JPJavaFrame::NewIntArray(jsize len)
{
	JAVA_RETURN(jintArray, "JPJavaFrame::NewIntArray",
		m_Env->functions->NewIntArray(m_Env, len));
}

void JPJavaFrame::SetIntArrayRegion(jintArray array, jsize start, jsize len, jint* vals)
{
	JAVA_CHECK("JPJavaFrame::SetIntArrayRegion",
		m_Env->functions->SetIntArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetIntArrayRegion(jintArray array, jsize start, jsize len, jint* vals)
{
	JAVA_CHECK("JPJavaFrame::GetIntArrayRegion",
		m_Env->functions->GetIntArrayRegion(m_Env, array, start, len, vals));
}

jint* JPJavaFrame::GetIntArrayElements(jintArray array, jboolean* isCopy)
{
	JAVA_RETURN(jint*, "JPJavaFrame::GetIntArrayElements",
		m_Env->functions->GetIntArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseIntArrayElements(jintArray array, jint* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseIntArrayElements",
		m_Env->functions->ReleaseIntArrayElements(m_Env, array, v, mode));
}

jlongArray JPJavaFrame::NewLongArray(jsize len)
{
	JAVA_RETURN(jlongArray, "JPJavaFrame::NewLongArray",
		m_Env->functions->NewLongArray(m_Env, len));
}

void JPJavaFrame::SetLongArrayRegion(jlongArray array, jsize start, jsize len, jlong* vals)
{
	JAVA_CHECK("JPJavaFrame::SetLongArrayRegion",
		m_Env->functions->SetLongArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetLongArrayRegion(jlongArray array, jsize start, jsize len, jlong* vals)
{
	JAVA_CHECK("JPJavaFrame::GetLongArrayRegion",
		m_Env->functions->GetLongArrayRegion(m_Env, array, start, len, vals));
}

jlong* JPJavaFrame::GetLongArrayElements(jlongArray array, jboolean* isCopy)
{
	JAVA_RETURN(jlong*, "JPJavaFrame::GetLongArrayElements",
		m_Env->functions->GetLongArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseLongArrayElements(jlongArray array, jlong* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseLongArrayElements",
		m_Env->functions->ReleaseLongArrayElements(m_Env, array, v, mode));
}

jfloatArray JPJavaFrame::NewFloatArray(jsize len)
{
	JAVA_RETURN(jfloatArray, "JPJavaFrame::NewFloatArray",
		m_Env->functions->NewFloatArray(m_Env, len));
}

void JPJavaFrame::SetFloatArrayRegion(jfloatArray array, jsize start, jsize len, jfloat* vals)
{
	JAVA_CHECK("JPJavaFrame::SetFloatArrayRegion",
		m_Env->functions->SetFloatArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetFloatArrayRegion(jfloatArray array, jsize start, jsize len, jfloat* vals)
{
	JAVA_CHECK("JPJavaFrame::GetFloatArrayRegion",
		m_Env->functions->GetFloatArrayRegion(m_Env, array, start, len, vals));
}

jfloat* JPJavaFrame::GetFloatArrayElements(jfloatArray array, jboolean* isCopy)
{
	JAVA_RETURN(jfloat*, "JPJavaFrame::GetFloatArrayElements",
		m_Env->functions->GetFloatArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseFloatArrayElements(jfloatArray array, jfloat* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseFloatArrayElements",
		m_Env->functions->ReleaseFloatArrayElements(m_Env, array, v, mode));
}

jdoubleArray JPJavaFrame::NewDoubleArray(jsize len)
{
	JAVA_RETURN(jdoubleArray, "JPJavaFrame::NewDoubleArray",
		m_Env->functions->NewDoubleArray(m_Env, len));
}

void JPJavaFrame::SetDoubleArrayRegion(jdoubleArray array, jsize start, jsize len, jdouble* vals)
{
	JAVA_CHECK("JPJavaFrame::SetDoubleArrayRegion",
		m_Env->functions->SetDoubleArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetDoubleArrayRegion(jdoubleArray array, jsize start, jsize len, jdouble* vals)
{
	JAVA_CHECK("JPJavaFrame::GetDoubleArrayRegion",
		m_Env->functions->GetDoubleArrayRegion(m_Env, array, start, len, vals));
}

jdouble* JPJavaFrame::GetDoubleArrayElements(jdoubleArray array, jboolean* isCopy)
{
	JAVA_RETURN(jdouble*, "JPJavaFrame::GetDoubleArrayElements",
		m_Env->functions->GetDoubleArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseDoubleArrayElements(jdoubleArray array, jdouble* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseDoubleArrayElements",
		m_Env->functions->ReleaseDoubleArrayElements(m_Env, array, v, mode));
}

jcharArray JPJavaFrame::NewCharArray(jsize len)
{
	JAVA_RETURN(jcharArray, "JPJavaFrame::NewCharArray",
		m_Env->functions->NewCharArray(m_Env, len));
}

void JPJavaFrame::SetCharArrayRegion(jcharArray array, jsize start, jsize len, jchar* vals)
{
	JAVA_CHECK("JPJavaFrame::SetCharArrayRegion",
		m_Env->functions->SetCharArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetCharArrayRegion(jcharArray array, jsize start, jsize len, jchar* vals)
{
	JAVA_CHECK("JPJavaFrame::GetCharArrayRegion",
		m_Env->functions->GetCharArrayRegion(m_Env, array, start, len, vals));
}

jchar* JPJavaFrame::GetCharArrayElements(jcharArray array, jboolean* isCopy)
{
	JAVA_RETURN(jchar*, "JPJavaFrame::GetCharArrayElements",
		m_Env->functions->GetCharArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseCharArrayElements(jcharArray array, jchar* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseCharArrayElements",
		m_Env->functions->ReleaseCharArrayElements(m_Env, array, v, mode));
}

jbooleanArray JPJavaFrame::NewBooleanArray(jsize len)
{
	JAVA_RETURN(jbooleanArray, "JPJavaFrame::NewBooleanArray",
		m_Env->functions->NewBooleanArray(m_Env, len));
}

void JPJavaFrame::SetBooleanArrayRegion(jbooleanArray array, jsize start, jsize len, jboolean* vals)
{
	JAVA_CHECK("JPJavaFrame::SetBooleanArrayRegion",
		m_Env->functions->SetBooleanArrayRegion(m_Env, array, start, len, vals));
}

void JPJavaFrame::GetBooleanArrayRegion(jbooleanArray array, jsize start, jsize len, jboolean* vals)
{
	JAVA_CHECK("JPJavaFrame::GetBooleanArrayRegion",
		m_Env->functions->GetBooleanArrayRegion(m_Env, array, start, len, vals));
}

jboolean* JPJavaFrame::GetBooleanArrayElements(jbooleanArray array, jboolean* isCopy)
{
	JAVA_RETURN(jboolean*, "JPJavaFrame::GetBooleanArrayElements",
		m_Env->functions->GetBooleanArrayElements(m_Env, array, isCopy));
}

void JPJavaFrame::ReleaseBooleanArrayElements(jbooleanArray array, jboolean* v, jint mode)
{
	JAVA_CHECK("JPJavaFrame::ReleaseBooleanArrayElements",
		m_Env->functions->ReleaseBooleanArrayElements(m_Env, array, v, mode));
}

int JPJavaFrame::MonitorEnter(jobject a0)
{
	JAVA_RETURN(int, "JPJavaFrame::MonitorEnter",
		m_Env->functions->MonitorEnter(m_Env, a0));
}

int JPJavaFrame::MonitorExit(jobject a0)
{
	JAVA_RETURN(int, "JPJavaFrame::MonitorExit",
		m_Env->functions->MonitorExit(m_Env, a0));
}

jmethodID JPJavaFrame::FromReflectedMethod(jobject a0)
{
	JAVA_RETURN(jmethodID, "JPJavaFrame::FromReflectedMethod",
		m_Env->functions->FromReflectedMethod(m_Env, a0));
}

jfieldID JPJavaFrame::FromReflectedField(jobject a0)
{
	JAVA_RETURN(jfieldID, "JPJavaFrame::FromReflectedField",
		m_Env->functions->FromReflectedField(m_Env, a0));
}

jclass JPJavaFrame::FindClass(const string& a0)
{
	JAVA_RETURN(jclass, "JPJavaFrame::FindClass",
		m_Env->functions->FindClass(m_Env, a0.c_str()));
}

jobjectArray JPJavaFrame::NewObjectArray(jsize a0, jclass a1, jobject a2)
{
	JAVA_RETURN(jobjectArray, "JPJavaFrame::NewObjectArray",
		m_Env->functions->NewObjectArray(m_Env, a0, a1, a2));
}

void JPJavaFrame::SetObjectArrayElement(jobjectArray a0, jsize a1, jobject a2)
{
	JAVA_CHECK("JPJavaFrame::SetObjectArrayElement",
		m_Env->functions->SetObjectArrayElement(m_Env, a0, a1, a2));
}

void JPJavaFrame::CallStaticVoidMethodA(jclass a0, jmethodID a1, jvalue* a2)
{
	JAVA_CHECK("JPJavaFrame::CallStaticVoidMethodA",
		m_Env->functions->CallStaticVoidMethodA(m_Env, a0, a1, a2));
}

void JPJavaFrame::CallVoidMethodA(jobject a0, jmethodID a1, jvalue* a2)
{
	JAVA_CHECK("JPJavaFrame::CallVoidMethodA",
		m_Env->functions->CallVoidMethodA(m_Env, a0, a1, a2));
}

void JPJavaFrame::CallNonvirtualVoidMethodA(jobject a0, jclass a1, jmethodID a2, jvalue* a3)
{
	JAVA_CHECK("JPJavaFrame::CallVoidMethodA",
		m_Env->functions->CallNonvirtualVoidMethodA(m_Env, a0, a1, a2, a3));
}

jboolean JPJavaFrame::IsAssignableFrom(jclass a0, jclass a1)
{
	JAVA_RETURN(jboolean, "JPJavaFrame::IsAssignableFrom",
		m_Env->functions->IsAssignableFrom(m_Env, a0, a1));
}

jstring JPJavaFrame::NewStringUTF(const char* a0)
{
	JAVA_RETURN(jstring, "JPJavaFrame::NewString",
		m_Env->functions->NewStringUTF(m_Env, a0));
}

const char* JPJavaFrame::GetStringUTFChars(jstring a0, jboolean* a1)
{
	JAVA_RETURN(const char*, "JPJavaFrame::GetStringUTFChars",
		m_Env->functions->GetStringUTFChars(m_Env, a0, a1));
}

void JPJavaFrame::ReleaseStringUTFChars(jstring a0, const char* a1)
{
	JAVA_CHECK("JPJavaFrame::ReleaseStringUTFChars",
		m_Env->functions->ReleaseStringUTFChars(m_Env, a0, a1));
}

jsize JPJavaFrame::GetArrayLength(jarray a0)
{
	JAVA_RETURN(jsize, "JPJavaFrame::GetArrayLength",
		m_Env->functions->GetArrayLength(m_Env, a0));
}

jobject JPJavaFrame::GetObjectArrayElement(jobjectArray a0, jsize a1)
{
	JAVA_RETURN(jobject, "JPJavaFrame::GetObjectArrayElement",
		m_Env->functions->GetObjectArrayElement(m_Env, a0, a1));
}

jmethodID JPJavaFrame::GetMethodID(jclass a0, const char* a1, const char* a2)
{
	JAVA_RETURN(jmethodID, "JPJavaFrame::GetMethodID",
		m_Env->functions->GetMethodID(m_Env, a0, a1, a2));
}

jmethodID JPJavaFrame::GetStaticMethodID(jclass a0, const char* a1, const char* a2)
{
	JAVA_RETURN(jmethodID, "JPJavaFrame::GetStaticMethodID",
		m_Env->functions->GetStaticMethodID(m_Env, a0, a1, a2));
}

jfieldID JPJavaFrame::GetFieldID(jclass a0, const char* a1, const char* a2)
{
	JAVA_RETURN(jfieldID, "JPJavaFrame::GetFieldID",
		m_Env->functions->GetFieldID(m_Env, a0, a1, a2));
}

jfieldID JPJavaFrame::GetStaticFieldID(jclass a0, const char* a1, const char* a2)
{
	JAVA_RETURN(jfieldID, "JPJavaFrame::GetStaticFieldID",
		m_Env->functions->GetStaticFieldID(m_Env, a0, a1, a2));
}

jsize JPJavaFrame::GetStringUTFLength(jstring a0)
{
	JAVA_RETURN(jsize, "JPJavaFrame::GetStringUTFLength",
		m_Env->functions->GetStringUTFLength(m_Env, a0));
}

jclass JPJavaFrame::DefineClass(const char* a0, jobject a1, const jbyte* a2, jsize a3)
{
	JAVA_RETURN(jclass, "JPJavaFrame::DefineClass",
		m_Env->functions->DefineClass(m_Env, a0, a1, a2, a3));
}

jint JPJavaFrame::RegisterNatives(jclass a0, const JNINativeMethod* a1, jint a2)
{
	JAVA_RETURN(jint, "JPJavaFrame::RegisterNatives",
		m_Env->functions->RegisterNatives(m_Env, a0, a1, a2));
}

void* JPJavaFrame::GetDirectBufferAddress(jobject obj)
{
	JAVA_RETURN(void*, "JPJavaFrame::GetDirectBufferAddress",
		m_Env->functions->GetDirectBufferAddress(m_Env, obj));
}

jlong JPJavaFrame::GetDirectBufferCapacity(jobject obj)
{
	JAVA_RETURN(jlong, "JPJavaFrame::GetDirectBufferAddress",
		m_Env->functions->GetDirectBufferCapacity(m_Env, obj));
}

jboolean JPJavaFrame::isBufferReadOnly(jobject obj)
{
	return CallBooleanMethodA(obj, m_Context->m_Buffer_IsReadOnlyID, 0);
}

jboolean JPJavaFrame::orderBuffer(jobject obj)
{
	jvalue arg;
	arg.l = obj;
	return CallBooleanMethodA(m_Context->m_JavaContext.get(),
			m_Context->m_Context_OrderID, &arg);
}

// GCOVR_EXCL_START
// This is used when debugging reference counting problems.
jclass JPJavaFrame::getClass(jobject obj)
{
	return (jclass) CallObjectMethodA(obj, m_Context->m_Object_GetClassID, 0);
}
// GCOVR_EXCL_STOP

class JPStringAccessor
{
	JPJavaFrame& frame_;
	jboolean isCopy;

public:
	const char* cstr;
	int length;
	jstring jstr_;

	JPStringAccessor(JPJavaFrame& frame, jstring jstr)
	: frame_(frame), jstr_(jstr)
	{
		cstr = frame_.GetStringUTFChars(jstr, &isCopy);
		length = frame_.GetStringUTFLength(jstr);
	}

	~JPStringAccessor()
	{
		try
		{
			frame_.ReleaseStringUTFChars(jstr_, cstr);
		}		catch (JPypeException&)
		{
			// Error during release must be eaten.
			// If Java does not accept a release of the buffer it
			// is Java's issue, not ours.
		}
	}
} ;

string JPJavaFrame::toString(jobject o)
{
	jstring str = (jstring) CallObjectMethodA(o, m_Context->m_Object_ToStringID, 0);
	return toStringUTF8(str);
}

string JPJavaFrame::toStringUTF8(jstring str)
{
	JPStringAccessor contents(*this, str);
	return transcribe(contents.cstr, contents.length, JPEncodingJavaUTF8(), JPEncodingUTF8());
}

jstring JPJavaFrame::fromStringUTF8(const string& str)
{
	string mstr = transcribe(str.c_str(), str.size(), JPEncodingUTF8(), JPEncodingJavaUTF8());
	return (jstring) NewStringUTF(mstr.c_str());
}

jobject JPJavaFrame::toCharArray(jstring jstr)
{
	return CallObjectMethodA(jstr, m_Context->m_String_ToCharArrayID, 0);
}

bool JPJavaFrame::equals(jobject o1, jobject o2 )
{
	jvalue args;
	args.l = o2;
	return CallBooleanMethodA(o1, m_Context->m_Object_EqualsID, &args) != 0;
}

jint JPJavaFrame::hashCode(jobject o)
{
	return CallIntMethodA(o, m_Context->m_Object_HashCodeID, 0);
}

jobject JPJavaFrame::collectRectangular(jarray obj)
{
	if (m_Context->m_Context_collectRectangularID == 0)
		return 0;
	jvalue v;
	v.l = (jobject) obj;
	JAVA_RETURN(jobject, "JPJavaFrame::collectRectangular",
			CallObjectMethodA(
			m_Context->m_JavaContext.get(),
			m_Context->m_Context_collectRectangularID, &v));
}

jobject JPJavaFrame::assemble(jobject dims, jobject parts)
{
	if (m_Context->m_Context_collectRectangularID == 0)
		return 0;
	jvalue v[2];
	v[0].l = (jobject) dims;
	v[1].l = (jobject) parts;
	JAVA_RETURN(jobject, "JPJavaFrame::assemble",
			CallObjectMethodA(
			m_Context->m_JavaContext.get(),
			m_Context->m_Context_assembleID, v));
}

jobject JPJavaFrame::callMethod(jobject method, jobject obj, jobject args)
{
	JP_TRACE_IN("JPJavaFrame::callMethod");
	if (m_Context->m_CallMethodID == 0)
		return NULL;
	JPJavaFrame frame(*this);
	jvalue v[3];
	v[0].l = method;
	v[1].l = obj;
	v[2].l = args;
	return frame.keep(frame.CallObjectMethodA(m_Context->m_JavaContext.get(), m_Context->m_CallMethodID, v));
	JP_TRACE_OUT;
}

JPClass *JPJavaFrame::findClass(jclass obj)
{
	return m_Context->getTypeManager()->findClass(obj);
}

JPClass *JPJavaFrame::findClassByName(const string& name)
{
	return m_Context->getTypeManager()->findClassByName(name);
}

JPClass *JPJavaFrame::findClassForObject(jobject obj)
{
	return m_Context->getTypeManager()->findClassForObject(obj);
}

jint JPJavaFrame::compareTo(jobject obj, jobject obj2)
{
	jvalue v;
	v.l = obj2;
	return this->CallIntMethodA(obj, m_Context->m_CompareToID, &v);
}
